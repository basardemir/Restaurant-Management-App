from flask import Flask, url_for, redirect, request, render_template
#from passlib.hash import pbkdf2_sha256 as hasher
import datetime
from flask import current_app
from flask_login import UserMixin, LoginManager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    return get_user(user_id)

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.active = True
        self.is_admin = False

    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return self.active


def users_page():
    testusers = [{"name": "Ali", "date": datetime.datetime.now()}]
    return render_template("/users/read.html", users = testusers)

def add_user_page():
    if request.method == "GET":
        print("Add a user")
        return render_template("/users/create.html")
    else:
        print("POSTED:")
        data = {"username": request.form['username'], "password": request.form["password"]}
        print(data)
        return redirect(url_for("users_page"))

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

def signin_page():
    if request.method == "GET":
        print("Add a user")
        return render_template("/users/login.html")
    else:
        print("POSTED:")
        data = {"username": request.form['username'], "password": request.form["password"]}
        form = LoginForm()
        if form.validate_on_submit():
            username = form.data["username"]
            user = get_user(username)
            if user is not None:
                password = form.data["password"]
                if hasher.verify(password, user.password):
                    login_user(user)
                    flash("You have logged in.")
                    next_page = request.args.get("next", url_for("users_page"))
                    return redirect(next_page)
            flash("Invalid credentials.")
        return render_template("/users/read.html", form=form)
        print(data)
        return redirect(url_for("users_page"))