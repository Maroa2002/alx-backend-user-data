#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, jsonify, request, abort
from flask import make_response, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def index():
    """/ route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """/users route"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """/sessions route"""
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        return jsonify({"message": "email and password required"}), 400
    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = make_response(
        jsonify({"email": email, "message": "logged in"})
    )
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=['DELETE'])
def logout():
    """DELETE /sessions route"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for("index"))
    else:
        abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    """/profile route"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route("/reset_password", methods=['POST'])
def get_reset_password_token():
    email = request.form.get("email")
    if not email:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route("/reset_password", methods=['PUT'])
def update_password():
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
