from web import app
from flask import jsonify, request
from web.model import Hardware, Configuration, Command, Schedule, Response, User
from config import Config
from flask_jwt_extended import jwt_required

"""
Each model has 5 routes accessing it:
    - index: to GET all the rows of the table
    - post: to add a new row in the database
    - put: to edit an existing row
    - delete: to delete an existing row
    - get: to get one row of the database
"""


@app.route("/")
def index():
    return jsonify({"message": "hello :D"})



"""
HARDWARE: REEM
"""
@app.route("/hardware", methods=["GET"])
@jwt_required
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


"""
CONFIGURATION: ABEER
"""
@app.route("/configuration", methods=["GET"])
def configuration_index():
    return jsonify(Configuration.index())


@app.route("/configuration", methods=["POST"])
def configuration_post():
    body = request.get_json()
    obj = Configuration.post(body)
    return {"message": Config.POST_MESSAGE, "object": obj}, 201


@app.route("/configuration/<_id>", methods=["GET"])
def configuration_get(_id):
    obj = Configuration.get({"id": _id})
    return jsonify(obj)


@app.route("/configuration/<_id>", methods=["DELETE"])
def configuration_delete(_id):
    Configuration.delete({"id": _id})
    return {"message": Config.DELETE_MESSAGE}, 203


@app.route("/configuration/<_id>", methods=["PUT"])
def configuration_put(_id):
    body = request.get_json()
    obj = Configuration.put({"id": _id}, body)
    return {"message": Config.PUT_MESSAGE, "object": obj}


"""
COMMAND: SARAH
"""
@app.route("/command", methods=["GET"])
def command_index():
    return jsonify(Command.index())


@app.route("/command", methods=["POST"])
def command_post():
    body = request.get_json()
    obj = Command.post(body)
    return {"message": Config.POST_MESSAGE, "object": obj}, 201


@app.route("/command/<_id>", methods=["GET"])
def command_get(_id):
    obj = Command.get({"id": _id})
    return jsonify(obj)


@app.route("/command/<_id>", methods=["DELETE"])
def command_delete(_id):
    Command.delete({"id": _id})
    return {"message": Config.DELETE_MESSAGE}, 203


@app.route("/command/<_id>", methods=["PUT"])
def command_put(_id):
    body = request.get_json()
    obj = Command.put({"id": _id}, body)
    return {"message": Config.PUT_MESSAGE, "object": obj}


"""
SCHEDULE: NOUF
"""
@app.route("/schedule", methods=["GET"])
def schedule_index():
    return jsonify(Schedule.index())


@app.route("/schedule", methods=["POST"])
def schedule_post():
    body = request.get_json()
    obj = Schedule.post(body)
    return {"message": Config.POST_MESSAGE, "object": obj}, 201


@app.route("/schedule/<_id>", methods=["GET"])
def schedule_get(_id):
    obj = Schedule.get({"id": _id})
    return jsonify(obj)


@app.route("/schedule/<_id>", methods=["DELETE"])
def schedule_delete(_id):
    Schedule.delete({"id": _id})
    return {"message": Config.DELETE_MESSAGE}, 203


@app.route("/schedule/<_id>", methods=["PUT"])
def schedule_put(_id):
    body = request.get_json()
    obj = Schedule.put({"id": _id}, body)
    return {"message": Config.PUT_MESSAGE, "object": obj}


"""
RESPONSE: MONA
"""
@app.route("/response", methods=["GET"])
def response_index():
    return jsonify(Response.index())


@app.route("/response", methods=["POST"])
def response_post():
    body = request.get_json()
    obj = Response.post(body)
    return {"message": Config.POST_MESSAGE, "object": obj}, 201


@app.route("/response/<_id>", methods=["GET"])
def response_get(_id):
    obj = Response.get({"id": _id})
    return jsonify(obj)


@app.route("/response/<_id>", methods=["DELETE"])
def response_delete(_id):
    Response.delete({"id": _id})
    return {"message": Config.DELETE_MESSAGE}, 203


@app.route("/response/<_id>", methods=["PUT"])
def response_put(_id):
    body = request.get_json()
    obj = Response.put({"id": _id}, body)
    return {"message": Config.PUT_MESSAGE, "object": obj}



"""
USER: REEM
"""
@app.route("/user", methods=["GET"])
def user_index():
    return jsonify(User.index())


@app.route("/user", methods=["POST"])
def user_post():
    body = request.get_json()
    obj = User.post(body)
    return {"message": Config.POST_MESSAGE, "object": obj}, 201


@app.route("/user/<_id>", methods=["GET"])
def user_get(_id):
    obj = User.get({"id": _id})
    return jsonify(obj)


@app.route("/user/<_id>", methods=["DELETE"])
def user_delete(_id):
    User.delete({"id": _id})
    return {"message": Config.DELETE_MESSAGE}, 203


@app.route("/user/<_id>", methods=["PUT"])
@jwt_required
def user_put(_id):
    body = request.get_json()
    obj = User.put({"id": _id}, body)
    return {"message": Config.PUT_MESSAGE, "object": obj}
