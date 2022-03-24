import os
from flask_socketio import SocketIO

from flask import Flask, render_template
from importer import Importer

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "SECRET!!!")
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("create_episode")
def create_episode(data):
    app.logger.info('start creating episode')
    Importer(app.logger).do_import(data["password"])


if __name__ == "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    socketio.run(app)
