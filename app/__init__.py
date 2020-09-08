# wsimple api part
from .api import Wsimple

# wsimple webserver part
if not __name__ == "__main__":
    #flask/flask-addon libraries
    from flask import Flask, render_template, redirect, session, g
    from flask_socketio import SocketIO
    from flask_session import Session
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
    #standard library
    from threading import Lock
    import sqlite3
    import pathlib
    import os

    # export FLASK_APP=Wsimple/app.py
    # export FLASK_ENV=development

    app = Flask(__name__)
    socketio = SocketIO(app, manage_session=False)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config["DEBUG"] = True
    app.config["DEVELOPMENT"] = True
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)
    thread = None
    thread_lock = Lock()
    featured = ["SPY", "DDOG", "EBAY", "GOOGL"]

    DATABASE = pathlib.Path(__file__).cwd() / "wsimple.db"

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
        socketio.run(app)