from flask import Flask, render_template, url_for, redirect
from get_info import getNewInfo, getLoadedInfo, getPlayerInfo

app = Flask(__name__)


@app.route("/")
@app.route("/player")
def home():
    info = getLoadedInfo("player-info.json")
    return render_template("main.html", title="Get all your info here!", info=info)


@app.route("/player/<playertag>")
def player(playertag):
    info = getPlayerInfo("#" + playertag)
    return render_template("main.html", title=info["name"], info=info)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
