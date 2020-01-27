from web import app
from flask import jsonify


thisdict ={
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}


@app.route("/1")
def reem():
    x = thisdict["model"]
    return jsonify(x)