from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "ahoj sv"


@app.route("/haha")
def druha_funkce():
    return "jen se nesmej"


if __name__ == "__main__":
    app.run(debug=True)
