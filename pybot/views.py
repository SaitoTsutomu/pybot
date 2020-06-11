from pathlib import Path

import toml

from flask import Flask, render_template, session

version = "0.0.1"

app = Flask(__name__)
app.config.from_object("pybot.config")
cwd = Path(__file__).parent
data = toml.load(str(cwd / "data.toml"))


def main():
    app.run(app.config.get("HOST"), app.config.get("PORT"), use_reloader=True)


@app.route("/")
def index():
    return render_template("index.html", command=session.get("command", ""))
