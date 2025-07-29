import flask
from flask import jsonify, request, render_template, make_response, send_file, send_from_directory, current_app, abort, redirect, url_for
import redis
from scripts.pdf import erstelle_latex_pdf
from scripts.user_setup import set_up_user
from server_config import *

views = flask.Blueprint(__name__, "views")

@views.before_request
def before():
    if (request.cookies.get(COOKIE_KEY) == SECRET_KEY):
        pass
    else:
        r = redis.Redis(host='localhost', port=6379, db=0)
        shutting_down = r.get("SHUTTING_DOWN")
        if shutting_down and shutting_down.decode() == "true":
            return jsonify(message="Server is shutting down"), 503

@views.route("/")
def main():
    tmp_user = set_up_user(request, make_response(render_template("main/index.html")))
    return tmp_user.response

@views.route("/projects")
def projects():
    tmp_user = set_up_user(request, make_response(render_template("main/projects.html")))
    return tmp_user.response

@views.route("/profile")
def profile():
    tmp_user = set_up_user(request, make_response(render_template("auth/profile.html")))
    if tmp_user.rank == 'client':
        abort(401)
    else:
        return tmp_user.response

@views.route("/pdf")
def pdf():
    tmp_user = set_up_user(request, make_response(render_template("auth/profile.html")))
    if tmp_user.rank == 'client':
        abort(401)
    erstelle_latex_pdf("nutzer_info", {"Name": "Felix", "Alter": 21, "Stadt": "Jugenheim"})
    return send_file("nutzer_info.pdf")


@views.route("/io")
def io():
    tmp_user = set_up_user(request, redirect(url_for('views.main')))
    if tmp_user.rank != "admin":
        abort(401)
    r = redis.Redis(host='localhost', port=6379, db=0)
    shutting_down = r.get("SHUTTING_DOWN")
    if shutting_down and shutting_down.decode() == "true":
        r.set("SHUTTING_DOWN", "false")
        return jsonify(message="Server wurde hochgefahren"), 503
    r.set("SHUTTING_DOWN", "true")
    return jsonify(message="Server wurde heruntergefahren")

@views.route("/<rest>")
def rest(rest):
    abort(401)