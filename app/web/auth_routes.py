from flask import flash, jsonify, redirect, render_template, request, session, url_for

from ..db import fetch_all_auth, fetch_one_auth
from .blueprint import bp
from .helpers import digits_only


@bp.route("/")
def root():
    if session.get("userid"):
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("main.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("userid"):
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        dob_pin = digits_only(password)

        row = fetch_one_auth(
            "SELECT * FROM users "
            "WHERE status='Active' AND name=%s "
            "AND REPLACE(REPLACE(COALESCE(dob, ''), '/', ''), '-', '')=%s "
            "LIMIT 1",
            (username, dob_pin),
        )
        if row:
            session["empname"] = row.get("name", "")
            session["userid"] = row.get("id", "")
            session["usertype"] = row.get("role", "")
            session["designation"] = row.get("designation", "")
            return redirect(url_for("main.dashboard"))

        flash("Invalid username/password", "error")

    return render_template("login.html")


@bp.route("/api/login-suggestions")
def login_suggestions():
    term = (request.args.get("q") or "").strip()
    if len(term) < 1:
        return jsonify([])

    rows = fetch_all_auth(
        "SELECT name AS login_id FROM users "
        "WHERE status='Active' AND name LIKE %s "
        "ORDER BY name ASC LIMIT 8",
        (f"%{term}%",),
    )
    return jsonify([r.get("login_id", "") for r in rows if r.get("login_id")])


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))
