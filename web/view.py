from sqlalchemy.exc import IntegrityError, InvalidRequestError

from web import app, db
from flask import jsonify, request, render_template
from web.model import Hardware, Command, Schedule, Response, User, Raspberry, RaspberryUser
from config import Config
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_

"""
error handling
"""


@app.errorhandler(400)
def error_400(error):
    return jsonify({'message': '{}'.format(error)}), 400


@app.errorhandler(401)
def error_401(error):
    return jsonify({'message': '{}'.format(error)}), 401


@app.errorhandler(403)
def error_403(error):
    return jsonify({'message': '{}'.format(error)}), 403


@app.errorhandler(405)
def error_405(error):
    return jsonify({'message': '{}'.format(error)}), 405


@app.errorhandler(404)
def error_404(error):
    return jsonify({'message': '{}'.format(error)}), 404


@app.errorhandler(409)
def error_409(error):
    return jsonify({'message': '{}'.format(error)}), 409


@app.errorhandler(422)
def error_422(error):
    return jsonify({'message': '{}'.format(error)}), 422


@app.errorhandler(500)
def error_500(error):
    return jsonify({'message': '{}'.format(error)}), 500


@app.route("/")
def index():
    # return render_template("actual_main.html")
    return jsonify({"message": "hello :D"})


@app.route("/privacy_policy")
def privacy():
    return render_template("privacy_policy.html")
    # return jsonify({"message": "hello :D"})


"""
Each model has 5 routes accessing it:
    - index: to GET all the rows of the table
    - post: to add a new row in the database
    - put: to edit an existing row
    - delete: to delete an existing row
    - get: to get one row of the database
"""


"""
HARDWARE: REEM
"""
@app.route("/hardware", methods=["GET"])
@jwt_required
def hardware_index():
    raspberry = request.args.get('raspberry_id')
    ids = {"raspberry_id": raspberry} if raspberry else {}
    return jsonify(Hardware.index(ids))


@app.route("/hardware", methods=["POST"])
@jwt_required
def hardware_post():
    try:
        body = request.get_json()
        obj = Hardware.post(body)
        return {"message": Config.POST_MESSAGE, "object": obj}, 201

    except InvalidRequestError:
        db.session().rollback()
        return jsonify({'message': 'an invalid request'}), 409
    except IntegrityError:
        return jsonify({'message': 'an integrity error occurred'}), 409


@app.route("/hardware/<_id>", methods=["GET"])
@jwt_required
def hardware_get(_id):
    raspberry = request.args.get('raspberry_id')
    ids = {"id": _id}
    if raspberry:
        ids["raspberry_id"] = raspberry
    obj = Hardware.get(ids)

    return jsonify(obj)


@app.route("/hardware/<_id>", methods=["DELETE"])
@jwt_required
def hardware_delete(_id):
    Hardware.delete({"id": _id})
    return {"message": Config.DELETE_MESSAGE}, 203


@app.route("/hardware/<_id>", methods=["PUT"])
@jwt_required
def hardware_put(_id):
    body = request.get_json()
    obj = Hardware.put({"id": _id}, body)
    return {"message": Config.PUT_MESSAGE, "object": obj}

#
# """
# CONFIGURATION: ABEER
# """
# @app.route("/configuration", methods=["GET"])
# def configuration_index():
#     return jsonify(Configuration.index())
#
#
# @app.route("/configuration", methods=["POST"])
# def configuration_post():
#     body = request.get_json()
#     obj = Configuration.post(body)
#     return {"message": Config.POST_MESSAGE, "object": obj}, 201
#
#
# @app.route("/configuration/<_id>", methods=["GET"])
# def configuration_get(_id):
#     obj = Configuration.get({"id": _id})
#     return jsonify(obj)
#
#
# @app.route("/configuration/<_id>", methods=["DELETE"])
# def configuration_delete(_id):
#     Configuration.delete({"id": _id})
#     return {"message": Config.DELETE_MESSAGE}, 203
#
#
# @app.route("/configuration/<_id>", methods=["PUT"])
# def configuration_put(_id):
#     body = request.get_json()
#     obj = Configuration.put({"id": _id}, body)
#     return {"message": Config.PUT_MESSAGE, "object": obj}


"""
COMMAND: SARAH
"""
@app.route("/command", methods=["GET"])
@jwt_required
def command_index():
    ids = {}
    raspberry = request.args.get('raspberry_id')
    hardware = request.args.get('hardware_id')
    schedule_id = request.args.get('schedule_id')
    if raspberry:
        obj = Command.query.join(Hardware).\
                            outerjoin(Response, Response.command_id==Command.id).\
                            filter(Hardware.raspberry_id==raspberry # first only return command for certain raspberry
                                    ,or_(Response.isDone==None, Response.isDone==False)
                                   ).all()
        return jsonify(obj)
    if hardware:
        ids["hardware_id"] = hardware
    if schedule_id and schedule_id == "not_null":
        print("no schedule")
        return jsonify(Command.index(ids, True))
    return jsonify(Command.index(ids))


@app.route("/command", methods=["POST"])
@jwt_required
def command_post():
    try:
        body = request.get_json()
        obj = Command.post(body)
        return {"message": Config.POST_MESSAGE, "object": obj}, 201
    except InvalidRequestError:
        db.session().rollback()
        return jsonify({'message': 'an invalid request'}), 409
    except IntegrityError:
        return jsonify({'message': 'an integrity error occurred'}), 409


@app.route("/command/<_id>", methods=["GET"])
@jwt_required
def command_get(_id):
    ids = {"id": _id}
    raspberry = request.args.get('raspberry_id')
    hardware = request.args.get('hardware_id')
    if raspberry:
        ids["raspberry_id"] = raspberry
    if hardware:
        ids["hardware_id"] = hardware
    obj = Command.get(ids)
    return jsonify(obj)


@app.route("/command/<_id>", methods=["DELETE"])
@jwt_required
def command_delete(_id):
    Command.delete({"id": _id})
    return {"message": Config.DELETE_MESSAGE}, 203


@app.route("/command/<_id>", methods=["PUT"])
@jwt_required
def command_put(_id):
    body = request.get_json()
    obj = Command.put({"id": _id}, body)
    return {"message": Config.PUT_MESSAGE, "object": obj}


"""
SCHEDULE: NOUF
"""
@app.route("/schedule", methods=["GET"])
@jwt_required
def schedule_index():
    return jsonify(Schedule.index())


@app.route("/schedule", methods=["POST"])
@jwt_required
def schedule_post():
    try:
        body = request.get_json()
        obj = Schedule.post(body)
        return {"message": Config.POST_MESSAGE, "object": obj}, 201
    except InvalidRequestError:
        db.session().rollback()
        return jsonify({'message': 'an invalid request'}), 409
    except IntegrityError:
        return jsonify({'message': 'an integrity error occurred'}), 409


@app.route("/schedule/<_id>", methods=["GET"])
@jwt_required
def schedule_get(_id):
    obj = Schedule.get({"id": _id})
    return jsonify(obj)


@app.route("/schedule/<_id>", methods=["DELETE"])
@jwt_required
def schedule_delete(_id):
    Schedule.delete({"id": _id})
    return {"message": Config.DELETE_MESSAGE}, 203


@app.route("/schedule/<_id>", methods=["PUT"])
@jwt_required
def schedule_put(_id):
    body = request.get_json()
    obj = Schedule.put({"id": _id}, body)
    return {"message": Config.PUT_MESSAGE, "object": obj}


"""
RESPONSE: MONA
"""
@app.route("/response", methods=["GET"])
@jwt_required
def response_index():
    obj = Response.query.join(Command)\
        .join(Hardware).join(Raspberry) \
        .join(User, Raspberry.users)\
        .filter(User.id == get_jwt_identity())
    r_obj = obj.all()
    for response in obj:
        command = Command.query.filter_by(id=response.command_id, schedule_id=None).first()
        if command is not None:
            db.session.delete(command)
        db.session.delete(response)
    db.session.commit()
    return jsonify(r_obj)


@app.route("/response", methods=["POST"])
@jwt_required
def response_post():
    try:
        body = request.get_json()
        obj = Response.post(body)
        return {"message": Config.POST_MESSAGE, "object": obj}, 201
    except InvalidRequestError:
        db.session().rollback()
        return jsonify({'message': 'an invalid request'}), 409
    except IntegrityError:
        return jsonify({'message': 'an integrity error occurred'}), 409


@app.route("/response/<_id>", methods=["GET"])
@jwt_required
def response_get(_id):
    obj = Response.get({"id": _id})
    return jsonify(obj)


@app.route("/response/<_id>", methods=["DELETE"])
@jwt_required
def response_delete(_id):
    Response.delete({"id": _id})
    return {"message": Config.DELETE_MESSAGE}, 203


@app.route("/response/<_id>", methods=["PUT"])
@jwt_required
def response_put(_id):
    body = request.get_json()
    obj = Response.put({"id": _id}, body)
    return {"message": Config.PUT_MESSAGE, "object": obj}



"""
USER: REEM
"""
@app.route("/user", methods=["GET"])
@jwt_required
def user_index():
    raspberry_id = request.args.get('raspberry_id')
    if raspberry_id:
        obj = User.query.join(Raspberry, User.raspberries).filter(Raspberry.id == raspberry_id).all()
        return jsonify(obj)
    else:
        return jsonify(User.index())


@app.route("/user", methods=["POST"])
def user_post():
    try:
        body = request.get_json()
        obj = User.post(body)
        return {"message": Config.POST_MESSAGE, "object": obj}, 201
    except InvalidRequestError:
        db.session().rollback()
        return jsonify({'message': 'an invalid request'}), 409
    except IntegrityError:
        return jsonify({'message': 'an integrity error occurred'}), 409


@app.route("/user/<_id>", methods=["GET"])
@jwt_required
def user_get(_id):
    obj = User.get({"id": _id})
    return jsonify(obj)


@app.route("/user/<_id>", methods=["DELETE"])
@jwt_required
def user_delete(_id):
    User.delete({"id": _id})
    return {"message": Config.DELETE_MESSAGE}, 203


@app.route("/user/<_id>", methods=["PUT"])
@jwt_required
def user_put(_id):
    body = request.get_json()
    obj = User.put({"id": _id}, body)
    return {"message": Config.PUT_MESSAGE, "object": obj}



"""
RASPBERRY: REEM
"""
@app.route("/raspberry", methods=["GET"])
@jwt_required
def raspberry_index():
    user_id = request.args.get('user_id')
    if user_id:
        obj = Raspberry.query.join(User, Raspberry.users).filter(User.id == user_id).all()
        return jsonify(obj)
    else:
        return jsonify(Raspberry.index())


@app.route("/raspberry", methods=["POST"])
def raspberry_post():
    try:
        body = request.get_json()
        obj = Raspberry.post(body)
        return {"message": Config.POST_MESSAGE, "object": obj}, 201
    except InvalidRequestError:
        db.session().rollback()
        return jsonify({'message': 'an invalid request'}), 409
    except IntegrityError:
        return jsonify({'message': 'an integrity error occurred'}), 409


@app.route("/raspberry/<_id>", methods=["GET"])
@jwt_required
def raspberry_get(_id):
    obj = Raspberry.get({"id": _id})
    return jsonify(obj)


@app.route("/raspberry/<_id>", methods=["DELETE"])
@jwt_required
def raspberry_delete(_id):
    Raspberry.delete({"id": _id})
    return {"message": Config.DELETE_MESSAGE}, 203


@app.route("/raspberry/<_id>", methods=["PUT"])
@jwt_required
def raspberry_put(_id):
    body = request.get_json()
    obj = Raspberry.put({"id": _id}, body)
    return {"message": Config.PUT_MESSAGE, "object": obj}


@app.route("/raspberry_user", methods=["PUT"])
@jwt_required
def raspberry_user_put():
    body = request.get_json()
    obj = Raspberry.get({"id": body["raspberry_id"]})
    user = User.get({"id": get_jwt_identity()})
    user.raspberries.append(obj)
    db.session.commit()
    return {"message": Config.POST_MESSAGE, "object": obj}, 201


@app.route("/raspberry_user", methods=["DELETE"])
@jwt_required
def raspberry_user_delete():
    body = request.get_json()
    obj = Raspberry.get({"id": body["raspberry_id"]})
    user = User.get({"id": get_jwt_identity()})
    user.raspberries.remove(obj)
    db.session.commit()
    return {"message": Config.DELETE_MESSAGE}, 203
