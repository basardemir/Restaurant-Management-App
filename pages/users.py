from flask import Flask, url_for, redirect, request, session, render_template
#from passlib.hash import pbkdf2_sha256 as hasher
import datetime
from flask import current_app
from .forms.users_form import UserAccountForm, Combine
from models.users import create_user
import os
DB_URL = os.getenv("DATABASE_URL")

import psycopg2 as dbapi2
import psycopg2.extras




def users_page():
    connection=dbapi2.connect(DB_URL)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    statement = "SELECT * FROM SOCIALMEDIA FULL OUTER JOIN (SELECT * FROM CONTACTINFO FULL OUTER JOIN (SELECT * FROM PERSON FULL OUTER JOIN (SELECT * FROM USERACCOUNT JOIN MEMBERSHIP ON USERACCOUNT.membershiptype = MEMBERSHIP.id) AS T2 ON PERSON.id = T2.person) AS T3 ON CONTACTINFO.id = T3.contactinfo) AS T4 ON T4.socialmedia = SOCIALMEDIA.id;"
    cursor.execute(statement)
    userlist = cursor.fetchall()
    cursor.close()
    print(userlist)
    return render_template("/users/read.html", users = userlist)

def add_user_page():
    print("Add a user")
    useraccount = Combine()
    print(useraccount.data)
    if useraccount.validate_on_submit():
        print("POSTED:")
        data = {"username": useraccount.data["useraccount"]['username'], "password": useraccount.data["useraccount"]["password"], "phoneNumber": useraccount.data["contactinfo"]["phoneNumber"], "email": useraccount.data["contactinfo"]["email"], "fax": useraccount.data["contactinfo"]["fax"], "homePhone": useraccount.data["contactinfo"]["homePhone"], "workmail": useraccount.data["contactinfo"]["workmail"], "lastEntry": datetime.datetime.now(), "joinedDate": datetime.datetime.now(), "securityAnswer": useraccount.data["useraccount"]["securityAnswer"], "membership": 0, "name": useraccount.data["person"]["name"], "surname": useraccount.data["person"]["surname"], "gender": useraccount.data["person"]["gender"], "birthday": useraccount.data["person"]["birthday"], "education": useraccount.data["person"]["educationLevel"], "facebook": useraccount.data["socialmedia"]["facebook"], "twitter": useraccount.data["socialmedia"]["twitter"], "instagram": useraccount.data["socialmedia"]["instagram"], "discord": useraccount.data["socialmedia"]["discord"], "youtube": useraccount.data["socialmedia"]["youtube"], "googleplus": useraccount.data["socialmedia"]["googleplus"]}
        print(useraccount.data)
        if useraccount.data["useraccount"]["membershiptype"] == "Boss":
            data["membership"] = 1
        else:
            data["membership"] = 2
        #print(data)
        create_user(data)
        # connection=dbapi2.connect(url)
        # cursor = connection.cursor()
        # statement = "INSERT INTO SOCIALMEDIA (facebook, twitter, instagram, discord, youtube, googleplus) VALUES (%s, %s, %s, %s, %s, %s);"
        # cursor.execute(statement, (data["facebook"], data['twitter'], data["instagram"], data["discord"], data["youtube"], data["googleplus"]))
        # statement = "INSERT INTO CONTACTINFO (socialmedia, phoneNumber, email, fax, homePhone, workmail) VALUES ((SELECT SOCIALMEDIA.id FROM SOCIALMEDIA WHERE (facebook=%s and twitter=%s and instagram=%s and discord=%s and youtube=%s and googleplus=%s)), %s, %s, %s, %s, %s);"
        # cursor.execute(statement, (data["facebook"], data['twitter'], data["instagram"], data["discord"], data["youtube"], data["googleplus"], data['phoneNumber'], data["email"], data["fax"], data["homePhone"], data["workmail"]))
        # statement = "INSERT INTO PERSON (contactinfo, name, surname, birthDay, educationLevel, gender) VALUES ((SELECT CONTACTINFO.id FROM CONTACTINFO WHERE (phoneNumber=%s and email=%s and fax=%s and homePhone=%s and workmail=%s)), %s, %s, %s, %s, %s);"
        # cursor.execute(statement, (data['phoneNumber'], data["email"], data["fax"], data["homePhone"], data["workmail"], data["name"], data['surname'], data["birthday"], data["education"], data["gender"]))
        # statement = "INSERT INTO USERACCOUNT (person, lastEntry, username, password, joinedDate, securityAnswer, membershiptype) VALUES ((SELECT PERSON.id FROM PERSON WHERE (name=%s and surname=%s and birthDay=%s and educationLevel=%s and gender=%s)), %s, %s, %s, %s, %s, %s);"
        # cursor.execute(statement, (data["name"], data['surname'], data["birthday"], data["education"], data["gender"], data["lastEntry"], data['username'], data["password"], data["joinedDate"], data["securityAnswer"], data["Membership"]))
        # connection.commit()
        # session['username'] = data["username"]
        # session['password'] = data["password"]
        # session['logged_in'] = True
        return redirect(url_for("users_page"))
    return render_template("/users/create.html", form=useraccount)
    
def signin_page():
    if request.method == "GET":
        print("Add a user")
        return render_template("/users/login.html")
    else:
        print("POSTED:")
        data = {"username": request.form['username'], "password": request.form["password"]}
        print(data)
        connection=dbapi2.connect(DB_URL)
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

def profile_page():
    if request.method == "GET":
        connection=dbapi2.connect(DB_URL)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        statement = "SELECT * FROM SOCIALMEDIA FULL OUTER JOIN (SELECT * FROM CONTACTINFO FULL OUTER JOIN (SELECT * FROM PERSON FULL OUTER JOIN ((SELECT * FROM USERACCOUNT WHERE username=%s and password=%s) AS T1 JOIN MEMBERSHIP ON T1.membershiptype = MEMBERSHIP.id) AS T2 ON PERSON.id = T2.person) AS T3 ON CONTACTINFO.id = T3.contactinfo) AS T4 ON T4.socialmedia = SOCIALMEDIA.id;"
        cursor.execute(statement, (session["username"], session["password"]))
        user = cursor.fetchall()
        print(user[0])
        cursor.close()
        return render_template("/users/profile.html", user=user[0])    

def logout_page():
    if request.method == "POST":
        print("POSTED: logout")
        session['username'] = ""
        session['password'] = ''
        session['logged_in'] = False
        print(session)
        return redirect(url_for("home_page"))