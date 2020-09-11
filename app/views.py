import random

from app import app, session, render_template, redirect
from app import socketio, thread, thread_lock
from app.forms import LoginForm
from app.api import Wsimple
from app.api import LoginError

@app.route('/index', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def index():              
    form = LoginForm()
    if form.validate_on_submit():
        email = str(form.email.data)
        password = str(form.password.data)
        tos = form.tos.data
        if tos:
            try:
                login = Wsimple(email, password)
                session["key"] = ",".join([email, password])
                return redirect('/home') 
            except LoginError:
                return render_template('index.html', form=form, pass_auth=True) 
    return render_template('index.html', form=form, pass_auth=False)

@app.route('/home', methods=['POST', 'GET'])
def home():
    try:
        account = str(session["key"]).split(",")
        login = Wsimple.auth(account[0], account[1])
        if "OK" in login:
            return render_template("main.html")
    except KeyError:
        return redirect('/') 
    
@app.route('/search', methods=['POST', 'GET'])
def search():
    try:
        account = str(session["key"]).split(",")
        login = Wsimple.auth(account[0], account[1])
        if "OK" in login:
            return render_template("search.html")
    except KeyError:
        return redirect('/')     
    
@app.route('/search/<sec_id>', methods=['POST', 'GET']) 
def search_stock(sec_id):
    try:
        account = str(session["key"]).split(",")
        login = Wsimple.auth(account[0], account[1])
        if "OK" in login:  
            return render_template("stock.html")
    except KeyError:
        return redirect('/')    
    
@app.route('/activities', methods=['POST', 'GET'])
def activities():
    try:
        account = str(session["key"]).split(",")
        login = Wsimple.auth(account[0], account[1])
        if "OK" in login:
            return render_template("activities.html")
    except KeyError:
        return redirect('/')     
    
@app.route('/settings', methods=['POST', 'GET'])
def settings():
    try:
        account = str(session["key"]).split(",")
        login = Wsimple.auth(account[0], account[1])
        if "OK" in login:
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
    
def dash_main_info(key):
    """Example of how to send server generated events to clients."""
    while True:
        account = str(key).split(",")
        ws = Wsimple(account[0], account[1])
        dashboard = ws.dashboard()
        socketio.emit('main_dashboard_info', dashboard)
        socketio.sleep(10)   
        
def settings_info(key):
    """Example of how to send server generated events to clients."""
    while True:
        account = str(key).split(",")
        ws = Wsimple(account[0], account[1])
        settings = ws.settings()
        print(settings)
        socketio.emit('return_settings', settings)
        socketio.sleep(10)  
    
@socketio.on('dashboard')
def soc_dashboard():
    global thread
    with thread_lock:
        if thread is None:
            print("Starting dashboard")
            thread = socketio.start_background_task(dash_main_info, (session["key"]))
            
@socketio.on("get_settings")
def soc_settings(data):
    global thread
    with thread_lock:
        if thread is None:
            print("Starting settings")
            thread = socketio.start_background_task(settings_info, (session["key"]))
            
@socketio.on('find_security')
def soc_find_security(data):
    print('search for security {}'.format(data[0]))  
    account = str(session["key"]).split(",")
    ws = Wsimple(account[0], account[1]) 
    security = ws.find_securities(data[0])
    socketio.emit('return_security', [security])              
    
@socketio.on('get_security_info')
def soc_find_security(data):
    #not the best solution
    account = str(session["key"]).split(",")
    ws = Wsimple(account[0], account[1]) 
    sparkline = ws.find_securities_by_id_historical(data[0], "1d")
    security_info = ws.find_securities_by_id(data[0])
    position = ws.get_account()["results"][0]["position_quantities"]
    print(f'stock_info {security_info["stock"]["symbol"]}')
    socketio.sleep(20)
    socketio.emit('return_stock_info', [sparkline, security_info, position])  
    
@socketio.on("get_activities")
def soc_get_activities(data):
    account = str(session["key"]).split(",")
    ws = Wsimple(account[0], account[1])
    socketio.sleep(5)
    if data == []:
        socketio.emit('display_activities', ws.get_activities())
    else:
        socketio.emit('display_activities', ws.get_activities_bookmark(data[0]))
        
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