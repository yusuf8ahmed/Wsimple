# some how start flask using gunicorn
# gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 4 app:app
import os
import click

PORT, WORKERS = 5000, 4

def wsimple(port, workers):
    os.system(f"gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -b 127.0.0.1:{port} -w {workers} app:app")

if __name__ == "__main__":
    wsimple(PORT, WORKERS)