from flask import Flask, url_for, redirect, request, render_template
import datetime

def users_page():
    testusers = [{"name": "Ali", "date": datetime.datetime.now()}]
    return render_template("/users/read.html", users = testusers)

def add_user_page():
    if request.method == "GET":
        print("Add a user")
        return render_template("/users/create.html")
    else:
        print("POSTED:")
        data = request.form['title']
        print(data)
        return redirect(url_for("users_page"))