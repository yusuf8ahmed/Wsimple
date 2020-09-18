"""
 Project Name: Wsimple
 Copyright (c) 2020 Chromazmoves
 Released under the Tos of Wealthsimple Trade and Wsimple
"""
from gevent import monkey
monkey.patch_all()
# wsimple api part
from .api import Wsimple

# wsimple webserver part
if not __name__ == "__main__":
    #flask/flask-addon libraries
    import random
    from flask import Flask, render_template, redirect
    from flask import session, g, current_app
    from flask_socketio import SocketIO
    from flask_session import Session
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
    #standard library
    from threading import Lock
    import sqlite3
    import logging
    import pathlib
    import os

    # export FLASK_APP=Wsimple/app.py
    # export FLASK_ENV=development
    # kill $(lsof -ti:3000)

    app = Flask(__name__)
    socketio = SocketIO(app, manage_session=False, logger=True)
    build = "01/09/2020"
    app.debug = True
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)
    thread = None
    thread_lock = Lock()
    TIME = 5
    ALLOW_DASH = True
    ALLOW_STOCK_INFO = True
    ALLOW_SETTINGS = True
    DATABASE = pathlib.Path(__file__).cwd() / "wsimple.db"
    
    @app.errorhandler(404)
    def page_not_found(e):
        # 1. og two pointing # 3. error in matrix
        # 4. listen here you little shit        
        # 5. you cant ground spider-man # 6. class not found
        # 7. f are you doing # 8. searching for f's 
        
        image = [
            "https://static2.cbrimages.com/wordpress/wp-content/uploads/2019/03/Spider-Man-Pointing-Meme.jpg",    
            "https://i.imgflip.com/44kbg9.jpg",
            "https://i.imgflip.com/3mkw5n.jpg",       
            "https://i.kym-cdn.com/entries/icons/original/000/005/482/50sspider-man-meme.jpg",  
            "https://memegenerator.net/img/instances/63226656/error-404-class-not-found.jpg",
            "https://memegenerator.net/img/instances/24858103/i-dont-know-what-the-fuck-youre-doing-404-error.jpg",
            "https://memegenerator.net/img/instances/60418014/searching-for-fucks-error-404-fucks-not-found.jpg"
        ]
        return render_template('404.html', link=random.choice(image)), 404

    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
        return db

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    from app import views

    if __name__ == '__main__':
        socketio.run(app, debug=True)