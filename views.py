import flask
from flask import jsonify, request
import redis

views = flask.Blueprint(__name__, "views")

@views.before_request
def before():
    if (request.cookies.get("user") == "admin"):
        pass
    else:
        r = redis.Redis(host='localhost', port=6379, db=0)
        shutting_down = r.get("SHUTTING_DOWN")
        if shutting_down and shutting_down.decode() == "true":
            return jsonify(message="Server is shutting down"), 503

@views.route("/")
def main():
    return "Moin"

@views.route("/io")
def io():
    r = redis.Redis(host='localhost', port=6379, db=0)
    shutting_down = r.get("SHUTTING_DOWN")
    if shutting_down and shutting_down.decode() == "true":
        r.set("SHUTTING_DOWN", "false")
        return jsonify(message="Server wurde hochgefahren"), 503
    r.set("SHUTTING_DOWN", "true")
    return jsonify(message="Server wurde heruntergefahren")