from flask import Flask, url_for, redirect, request, session, render_template
#from passlib.hash import pbkdf2_sha256 as hasher
import datetime
from flask import current_app

import psycopg2 as dbapi2

url = "postgres://ivpallnyfezioy:075baf8e129b0d52dbd6d87dd3c774363b0b10b499921f821378ed7084bfc744@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dagmb1jla3rmdp"



def users_page():
    #testusers = [{"name": "Ali", "date": datetime.datetime.now()}]]
    connection=dbapi2.connect(url)
    cursor = connection.cursor()
    statement = "SELECT * FROM USERACCOUNT;"
    cursor.execute(statement)
    userlist = cursor.fetchall()
    cursor.close()
    print(userlist)
    return render_template("/users/read.html", users = userlist)

def add_user_page():
    if request.method == "GET":
        print("Add a user")
        return render_template("/users/create.html")
    else:
        print("POSTED:")
        print(request.form)
        data = {"username": request.form['username'], "password": request.form["password"], "lastEntry": datetime.datetime.now(), "joinedDate": datetime.datetime.now(), "securityAnswer": request.form["securityQuestion"]}
        print(data)
        connection=dbapi2.connect(url)
        cursor = connection.cursor()
        statement = "INSERT INTO USERACCOUNT (lastEntry, username, password, joinedDate, securityAnswer) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(statement, (data["lastEntry"], data['username'], data["password"], data["joinedDate"], data["securityAnswer"]))
        connection.commit()
        session['username'] = data["username"]
        session['password'] = data["password"]
        session['logged_in'] = True
        return redirect(url_for("users_page"))


def signin_page():
    if request.method == "GET":
        print("Add a user")
        return render_template("/users/login.html")
    else:
        print("POSTED:")
        data = {"username": request.form['username'], "password": request.form["password"]}
        print(data)
        connection=dbapi2.connect(url)
        cursor = connection.cursor()
        statement = "SELECT * FROM USERACCOUNT;"
        cursor.execute(statement)
        userlist = cursor.fetchall()
        cursor.close()
        print(userlist)
        for item in userlist :
            if item[4] == data["username"] and item[5] == data["password"]:
                session['username'] = data["username"]
                session['password'] = data["password"]
                session['logged_in'] = True
        return redirect(url_for("users_page"))