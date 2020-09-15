import sys

from app import app, session, render_template, redirect
from app import socketio, thread, thread_lock, TIME
from app.forms import LoginForm
from app.api import Wsimple
from app.api import LoginError, InvalidAccessTokenError

@app.route('/index', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def index():              
    form = LoginForm()
    if form.validate_on_submit():
        email = str(form.email.data)
        password = str(form.password.data)
        print(email,password)
        tos = form.tos.data
        if tos:
            try:
                ws = Wsimple(email, password)
                session["key"] = ws.tokens
                return redirect('/home') 
            except LoginError:
                return render_template('index.html', form=form, pass_auth=True) 
    return render_template('index.html', form=form, pass_auth=False)

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
        # account = str(session["key"]).split(",")
        # login = Wsimple.auth(account[0], account[1])
        # if "OK" in login:  
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

#socket.io stuff
        
@socketio.on('connect')
def connect():
    print('Client connected')
    
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')  
    
def dash_main_info(tokens):
    """Example of how to send server generated events to clients."""
    ws = Wsimple.access(verbose=True)
    while True:
        try:
            socketio.sleep(TIME) 
            dashboard = ws.dashboard(tokens)
            socketio.emit('main_dashboard_info', dashboard, namespace='/dashboard')
        except InvalidAccessTokenError as e:
            print("dash_main_info invalid token")
            ws = Wsimple.access()
            new_tokens = ws.refresh_token(tokens)   
            print(f"dash_main_info re-valid token {new_tokens}")
            tokens = new_tokens                 
        
@socketio.on('dashboard', namespace='/dashboard')
def soc_dashboard():
    global thread
    with thread_lock:
        if thread is None:
            print("Starting dashboard")        
            if session.get('key') is not None:
                print("Starting dashboard true key") 
                thread = socketio.start_background_task(dash_main_info, session['key'])   
            else:
                print("Starting dashboard false key") 
                socketio.emit('invalid_token', namespace='/dashboard')
 
def settings_info(key):
    """Example of how to send server generated events to clients."""
    while True:
        ws = Wsimple.access()
        tokens = key
        settings = ws.settings(tokens)
        socketio.sleep(TIME) 
        socketio.emit('return_settings', settings)
        
@socketio.on("get_settings")
def soc_settings(data):
    global thread
    with thread_lock:
        if thread is None:
            print("Starting settings")
            thread = socketio.start_background_task(settings_info, (session["key"]))        
        
def stock_info(data):
    """Example of how to send server generated events to clients."""
    while True:
        try:
            ws = Wsimple.access()
            tokens = data[0]
            sparkline = ws.find_securities_by_id_historical(tokens, data[1], "1d")
            security_info = ws.find_securities_by_id(tokens, data[1])
            position = ws.get_account(tokens)
            socketio.sleep(TIME)
            socketio.emit('return_stock_info', [sparkline, security_info, position])
        except BaseException:
            print("stock_info InvalidAccessTokenError")
    
@socketio.on('get_security_info')
def soc_find_security(data):
    """
    not the best solution
    ws = Wsimple.access()
    tokens = session["key"]
    sparkline = ws.find_securities_by_id_historical(tokens, data[0], "1d")
    security_info = ws.find_securities_by_id(tokens, data[0])
    position = ws.get_account(tokens)["results"][0]["position_quantities"]
    print(f'stock_info {security_info["stock"]["symbol"]}')
    socketio.sleep(20)
    socketio.emit('return_stock_info', [sparkline, security_info, position])      
    """
    global thread
    with thread_lock:
        if thread is None:
            print("Starting settings")
            thread = socketio.start_background_task(stock_info, (session["key"], data))  
                
@socketio.on('find_security', namespace="/search")
def soc_find_security(data):
    print('search for security {}'.format(data[0]))  
    ws = Wsimple.access()
    tokens = session["key"]
    security = ws.find_securities(tokens, data[0])
    socketio.emit('return_security', [security], namespace="/search")              
    
@socketio.on("get_activities", namespace='/activities')
def soc_get_activities(data):
    ws = Wsimple.access()
    tokens = session["key"]
    socketio.sleep(5)
    if data == []:
        socketio.emit('display_activities', ws.get_activities(tokens), namespace='/activities')
    else:
        socketio.emit('display_activities', ws.get_activities_bookmark(tokens, data[0]), namespace='/activities')
        
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