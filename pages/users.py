from flask import Flask, url_for, redirect, request, session, render_template
#from passlib.hash import pbkdf2_sha256 as hasher
import datetime
from flask import current_app
from .forms.users_form import UserAccountForm, Combine, CallSocialMedia, CallContactInfo, CallPerson, CallUserAccount
from models.users import create_user, select_a_user, update_user, select_a_socialmedia, update_socialmedia, select_a_person, update_person, update_contactinfo, select_all_users_and_info, select_a_contactinfo
import os
DB_URL = os.getenv("DATABASE_URL")

import psycopg2 as dbapi2
import psycopg2.extras

url = "postgres://ivpallnyfezioy:075baf8e129b0d52dbd6d87dd3c774363b0b10b499921f821378ed7084bfc744@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dagmb1jla3rmdp"	



def users_page():
    userlist = select_all_users_and_info()
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
        if create_user(data):
            print("User created")
            session['username'] = data["username"]
            session['password'] = data["password"]
            session['logged_in'] = True
        else:
            print("User already exists")
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

def profile_page():
    if request.method == "GET":
        connection=dbapi2.connect(url)
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


def editsocialmedia_page():
    if session == {} or session["logged_in"] == False:
        return redirect(url_for("home_page"))
    data = select_a_socialmedia(session['username'], session['password'])
    form = CallSocialMedia()
    if request.method == "POST" and form.validate_on_submit():
        print("POSTED:")
        print(form.data)
        socialdata = form.data["socialmedia"]
        update_socialmedia(socialdata, session["username"], session["password"])
        return redirect(url_for("profile_page"))
    else:
        if data["facebook"] != None:
            form.socialmedia["facebook"].data = data["facebook"]
        if data["twitter"] != None:
            form.socialmedia["twitter"].data = data["twitter"]
        if data["instagram"] != None:
            form.socialmedia["instagram"].data = data["instagram"]
        if data["discord"] != None:
            form.socialmedia["discord"].data = data["discord"]
        if data["youtube"] != None:
            form.socialmedia["youtube"].data = data["youtube"]
        if data["googleplus"] != None:
            form.socialmedia["googleplus"].data = data["googleplus"]
    return render_template("/users/editsocialmedia.html", user=session, form=form, data = data)  

def editcontactinfo_page():
    if session == {} or session["logged_in"] == False:
        return redirect(url_for("home_page"))
    data = select_a_contactinfo(session['username'], session['password'])
    print(data)
    form = CallContactInfo()
    if request.method == "POST" and form.validate_on_submit():
        print("POSTED:")
        print(form.data)
        contactinfodata = form.data["contactinfo"]
        update_contactinfo(contactinfodata, session["username"], session["password"])
        return redirect(url_for("profile_page"))
    else:
        if data["phonenumber"] != None:
            form.contactinfo["phoneNumber"].data = data["phonenumber"]
        if data["email"] != None:
            form.contactinfo["email"].data = data["email"]
        if data["fax"] != None:
            form.contactinfo["fax"].data = data["fax"]
        if data["homephone"] != None:
            form.contactinfo["homePhone"].data = data["homephone"]
        if data["workmail"] != None:
            form.contactinfo["workmail"].data = data["workmail"]
    return render_template("/users/editcontactinfo.html", user=session, form=form, data = data)  

def editperson_page():
    if session == {} or session["logged_in"] == False:
        return redirect(url_for("home_page"))
    data = select_a_person(session['username'], session['password'])
    print(data)
    form = CallPerson()
    if request.method == "POST" and form.validate_on_submit():
        print("POSTED:")
        print(form.data)
        persondata = form.data["person"]
        update_person(persondata, session["username"], session["password"])
        return redirect(url_for("profile_page"))
    else:
        if data["name"] != None:
            form.person["name"].data = data["name"]
        if data["surname"] != None:
            form.person["surname"].data = data["surname"]
        if data["birthday"] != None:
            form.person["birthday"].data = data["birthday"]
        if data["educationlevel"] != None:
            form.person["educationLevel"].data = data["educationlevel"]
        if data["gender"] != None:
            form.person["gender"].data = data["gender"]
    return render_template("/users/editperson.html", user=session, form=form, data = data)  

def edituser_page():
    if session == {} or session["logged_in"] == False:
        return redirect(url_for("home_page"))
    data = select_a_user(session['username'], session['password'])
    form = CallUserAccount()
    if request.method == "POST" and form.validate_on_submit():
        userdata = form.data["user"]
        print(userdata)
        update_user(userdata, session["username"], session["password"])
        return redirect(url_for("profile_page"))
    else:
        if data["username"] != None:
            form.user["username"].data = data["username"]
        if data["securityanswer"] != None:
            form.user["securityAnswer"].data = data["securityanswer"]
    return render_template("/users/edituseraccount.html", user=session, form=form, data = data)  