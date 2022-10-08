from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password,password):
                flash("Logged in succesfuly", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Wrong password", category="error")
        else:
            flash("No user with this email exists", category="error")
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/sign_up", methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        valid = True
        if len(email) < 4:
            valid = False
            flash("Email must be at least 4 characters", category="error")
        elif User.query.filter_by(email=email).first():
            valid = False
            flash("Email already exists", category="error")
        if len(name) < 2:
            valid = False
            flash("Name must be at least 2 characters", category="error")
        if password1 != password2:
            valid = False
            flash("Passwords don't match", category="error")
        if len(password1) < 8:
            valid = False
            flash("Password must be at least 8 characters", category="error")
        if valid:
            # add to db
            new_user = User(email=email,name=name,password=generate_password_hash(password1,method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created", category="success")
            login_user(new_user, remember=True)
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)
