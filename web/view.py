from web import app, db
from flask import jsonify, render_template, request
from web.model import Hardware
from config import Config

"""
INDEX
POST
GET
PUT
DELETE
"""
@app.route("/hardware", methods=["GET"])
def hardware_index():
    return jsonify(Hardware.index())


@app.route("/hardware", methods=["POST"])
def hardware_post():
    body = request.get_json()
    obj = Hardware.post(body)
    return {"message": Config.POST_MESSAGE, "object": obj}, 201


@app.route("/hardware/<_id>", methods=["GET"])
def hardware_get(_id):
    obj = Hardware.get({"id": _id})
    return jsonify(obj)


@app.route("/hardware/<_id>", methods=["DELETE"])
def hardware_delete(_id):
    Hardware.delete({"id": _id})
    return {"message": Config.DELETE_MESSAGE}, 203


@app.route("/hardware/<_id>", methods=["PUT"])
def hardware_put(_id):
    body = request.get_json()
    obj = Hardware.put({"id": _id}, body)
    return {"message": Config.PUT_MESSAGE, "object": obj}


# thisdict = {
#   "brand": "Ford",
#   "model": "Mustang",
#   "year": 1964
# }
#
#
# @app.route("/1")
# def reem():
#     x = thisdict["model"]
#     return jsonify(x)
#
#
# @app.route("/hardware")
# def hardware_index():
#     hardwares = Hardware.query.all()
#     print(hardwares[0].name)
#     return jsonify(hardwares)
#
#
# @app.route("/")
# def index():
#     hardwares = Hardware.query.all()
#     return render_template('index.html', hardwares=hardwares, title="testing hardware")
