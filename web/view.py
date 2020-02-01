from web import app
from flask import jsonify, render_template
from web.model import Hardware

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}


@app.route("/1")
def reem():
    x = thisdict["model"]
    return jsonify(x)


@app.route("/hardware")
def hardware_index():
    hardwares = Hardware.query.all()
    print(hardwares[0].name)
    return jsonify(hardwares)


@app.route("/")
def index():
    hardwares = Hardware.query.all()
    return render_template('index.html', hardwares=hardwares, title="testing hardware")
