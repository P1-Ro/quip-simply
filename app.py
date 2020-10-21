from flask import Flask, render_template, request
from importer import do_import

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_episode', methods=["POST"])
def create_episode():
    password = request.form['password']
    do_import(password)
    return "OK", 200


if __name__ == '__main__':
    app.run()
