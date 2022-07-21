from flask import Flask, render_template, send_from_directory, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

from api.routes import api

load_dotenv()


app = Flask(__name__)
CORS(app)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/buffer")
def buffer():
    return render_template("buffer.html")

@app.route("/help")
def help():
    return render_template("help.html")



@app.route("/main_menu")
def main_menu():
    return render_template("main_menu.html")

@app.route("/loading")
def loading():
    return render_template("loading.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/")
def load():
    return render_template("loading.html")

@app.route("/output")
def output():
    return render_template("nodes.html")




# API routes
app.register_blueprint(api, url_prefix="/api")

if __name__ == '__main__':
    app.run()
