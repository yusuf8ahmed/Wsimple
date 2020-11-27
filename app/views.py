"""
 Project Name: Wsimple
 Copyright (c) 2020 Chromazmoves
"""
from app import app, session, render_template, redirect, logger
from app import socketio, thread, thread_lock
from app import ALLOW_DASH, ALLOW_SETTINGS, ALLOW_STOCK_INFO
from app import TIME_DASH, TIME_SETTINGS, TIME_STOCK_INFO
from app import threading, exit_dash_event, exit_search_event, exit_settings_event
from app.forms import LoginForm
from app.api import Wsimple
from app.api import LoginError 
from app.api import InvalidAccessTokenError, InvalidRefreshTokenError
from app.api import WSOTPUser, WSOTPError, WSOTPLoginError

@app.route('/index', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def index():              
    form = LoginForm()
    if form.validate_on_submit():
        email = str(form.email.data)
        password = str(form.password.data)
        token = str(form.token.data)
        print(email,password,token)
        tos = form.tos.data
        if tos:
            try:
                ws = Wsimple(email, password)
                session["key"] = ws.tokens
                return redirect('/home') 
            except WSOTPUser:
                # Wealthsimple OTP User
                if token:
                    try:
                        ws = Wsimple.otp_login(email, password, token)
                        session["key"] = ws.tokens
                        print(ws.tokens)
                        return redirect('/home') 
                    except WSOTPLoginError:
                        # Wealthsimple OTP User login error
                        return render_template('index.html', form=form, pass_auth=False, use_auth=False, show_auth_message=False)
                return render_template('index.html', form=form, pass_auth=False, use_auth=True, show_auth_message=True) 
            except LoginError:
                # enter worng password
                return render_template('index.html', form=form, pass_auth=True, use_auth=False, show_auth_message=False) 
    return render_template('index.html', form=form, pass_auth=False, use_auth=False, show_auth_message=False)

@app.route('/home', methods=['POST', 'GET'])
def home():
    try:
        # account = str(session["key"]).split(",")
        # login = Wsimple.auth(account[0], account[1])
        # if "OK" in login:
        return render_template("main.html")
    except KeyError:
        return redirect('/') 
    
@app.route('/search', methods=['POST', 'GET'])
def search():
    try:
        # account = str(session["key"]).split(",")
        # login = Wsimple.auth(account[0], account[1])
        # if "OK" in login:
        return render_template("search.html")
    except KeyError:
        return redirect('/')     
    
@app.route('/search/<sec_id>', methods=['POST', 'GET']) 
def search_stock(sec_id):
    try:
        print(f"route stock: {sec_id}")
        return render_template("stock.html")
    except KeyError:
        return redirect('/')    
    
@app.route('/activities', methods=['POST', 'GET'])
def activities():
    try:
        # account = str(session["key"]).split(",")
        # login = Wsimple.auth(account[0], account[1])
        # if "OK" in login:
        return render_template("activities.html")
    except KeyError:
        return redirect('/')     
    
@app.route('/settings', methods=['POST', 'GET'])
def settings():
    try:
        # account = str(session["key"]).split(",")
        # login = Wsimple.auth(account[0], account[1])
        # if "OK" in login:
        return render_template("settings.html")
    except KeyError:
        return redirect('/') 
    
@app.route('/tos', methods=['POST', 'GET'])
def tos():
    return render_template("tos.html")

@app.route('/index2.html', methods=['GET'])
def index2():
    return render_template("index2.html")
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        
@socketio.on('connect')
def connect():
    print('Client connected')
    
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')  
    
#? display the "/home" dashboard  
def dash_main_info(tokens):
    """Example of how to send server generated events to clients."""
    ws = Wsimple.access(verbose=True)
    while True:
        if exit_dash_event.is_set():
            logger.info("close event is set")
            break
        try:
            dashboard = ws.dashboard(tokens)
            socketio.sleep(TIME_DASH) 
            socketio.emit('main_dashboard_info', dashboard, namespace='/dashboard')              
        except InvalidAccessTokenError as e:
            try:
                print(f"dash_main_info invalid token {tokens}")
                ws = Wsimple.access()
                tokens = ws.refresh_token(tokens)   
                print(f"dash_main_info re-valid token {tokens}")  
            except InvalidRefreshTokenError as e:
                print(f"dash_main_info dead refresh token {tokens}")
                socketio.emit('invalid_token', namespace='/dashboard') 
                break 
            
@socketio.on('dashboard', namespace='/dashboard')
def soc_dashboard():
    global thread
    with thread_lock:
        if thread is None: 
            logger.info("Start dashboard")        
            if isinstance(session.get('key'), list):
                print(f"Starting dashboard key {session.get('key')}") 
                thread = socketio.start_background_task(dash_main_info, session['key'])   
            else:
                print("Starting dashboard false key") 
                socketio.emit('invalid_token', namespace='/dashboard')
                
@socketio.on('close_dash', namespace='/dashboard')
def soc_close_dashboard():
    logger.info("close event on dash")
    exit_dash_event.set()
 
#? display the stock info you searched
def stock_info(data):
    """Example of how to send server generated events to clients."""
    ws = Wsimple.access()
    tokens = data[0]
    sec_id = data[1]
    print(f"socket stock: {sec_id}")
    while True:
        try:
            re_stock_info = ws.stock(tokens, sec_id, time="1d")
            socketio.sleep(TIME_STOCK_INFO)
            socketio.emit('return_stock_info', re_stock_info, namespace='/stock')
        except InvalidAccessTokenError as e:
            try:
                print(f"stock_info invalid token {tokens}")
                ws = Wsimple.access()
                tokens = ws.refresh_token(tokens)   
                print(f"stock_info re-valid token {tokens}")  
            except InvalidRefreshTokenError as e:
                print(f"stock_info dead token {tokens}")  
                socketio.emit('invalid_token', namespace='/stock') 
                break 
    
@socketio.on('get_security_info', namespace='/stock')
def soc_stock_info(data): 
    global thread
    with thread_lock:
        if thread is None:
            logger.info("Start get_security_info")       
            if isinstance(session.get('key'), list):
                print(f"Starting stock_info key {session.get('key')}") 
                print((session['key'], data))
                thread = socketio.start_background_task(stock_info, (session['key'], data))   
            else:
                print("Starting stock_info false key") 
                socketio.emit('invalid_token', namespace='/stock')
 
#? display your settings  
def settings_info(key):
    """Example of how to send server generated events to clients."""
    while True:
        ws = Wsimple.access()
        tokens = key
        settings = ws.settings(tokens)
        socketio.sleep(TIME_SETTINGS) 
        socketio.emit('return_settings', settings, namespace="/settings")
        
@socketio.on("get_settings", namespace="/settings")
def soc_settings(data):
    global thread
    with thread_lock:
        if thread is None:
            logger.info("Start get_settings")
            thread = socketio.start_background_task(settings_info, (session["key"]))        
 
#? display the search page 
def search_page_info(tokens):
    """Example of how to send server generated events to clients."""
    ws = Wsimple.access(verbose=True)
    while True:
        try:
            settings = ws.search_page(tokens)
            socketio.sleep(TIME_STOCK_INFO) 
            socketio.emit('return_search_page', settings, namespace="/search")             
        except InvalidAccessTokenError as e:
            try:
                print(f"search_page_info invalid token {tokens}")
                ws = Wsimple.access()
                tokens = ws.refresh_token(tokens)   
                print(f"search_page_info re-valid token {tokens}")  
            except InvalidRefreshTokenError as e:
                print(f"search_page_info dead refresh token {tokens}")
                socketio.emit('invalid_token', namespace='/dashboard') 
                break
        
@socketio.on("get_search_page", namespace="/search")
def soc_search_page():
    global thread
    with thread_lock:
        if thread is None:
            logger.info("Start get_search_page")      
            if isinstance(session.get('key'), list):
                logger.info(f"Starting get_search_page key={session.get('key')}") 
                thread = socketio.start_background_task(search_page_info, (session["key"]))   
            else:
                logger.error("Starting stock_info false key") 
                socketio.emit('invalid_token', namespace='/search') 
  
#? display search securities          
@socketio.on('find_security', namespace="/search")
def soc_find_security(data):
    logger.info("Start search for security {}".format(data[0]))
    ws = Wsimple.access()
    tokens = session["key"]
    security = ws.find_securities(tokens, data[0])
    socketio.emit('return_security', [security], namespace="/search")              

#? display your activities
@socketio.on("get_activities", namespace='/activities')
def soc_get_activities(data):
    logger.info("Start search for activities")
    ws = Wsimple.access()
    tokens = session["key"]
    socketio.sleep(5)
    if data == []:
        socketio.emit('display_activities', ws.get_activities(tokens), namespace='/activities')
    else:
        socketio.emit('display_activities', ws.get_activities_bookmark(tokens, data[0]), namespace='/activities')
        
# orders sockets

@socketio.on("market_buy_order")
def soc_market_buy_order(data):
    socketio.emit('',)
   
@socketio.on("market_sell_order")
def soc_market_sell_order(data):
    socketio.emit('',)
    
@socketio.on("market_limit_buy_order")
def soc_market_limit_buy_order(data):
    socketio.emit('',)
    
@socketio.on("market_limit_sell_order")
def soc_market_limit_sell_order(data):
    socketio.emit('',)
    
@socketio.on("market_stop_limit_buy_order")
def soc_market_stop_limit_buy_order(data):
    socketio.emit('',)
    
@socketio.on("market_stop_limit_sell_order")
def soc_market_stop_limit_sell_order(data):
    socketio.emit('',)