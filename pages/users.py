from flask import Flask, url_for, redirect, request, session, render_template
from passlib.hash import pbkdf2_sha256 as hasher
import datetime
import json
from flask import current_app
from .forms.users_form import UserAccountForm, Combine, CallSocialMedia, CallContactInfo, CallPerson, CallUserAccount
from models.users import create_user, update_user_lastentry, select_users_membership_and_photo, select_users, select_a_user_and_info, delete_current_user, select_a_user, update_user, select_a_socialmedia, update_socialmedia, select_a_person, update_person, update_contactinfo, select_all_users_and_info, select_a_contactinfo
from models.location_model import get_all_location_with_dict
import os
DB_URL = os.getenv("DATABASE_URL")

import psycopg2 as dbapi2
import psycopg2.extras

url = "postgres://ivpallnyfezioy:075baf8e129b0d52dbd6d87dd3c774363b0b10b499921f821378ed7084bfc744@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dagmb1jla3rmdp"	



def users_page():
    userlist = select_users_membership_and_photo()
    return render_template("/users/read.html", users = userlist)

def add_user_page():
    if request.method == "GET":
        locations = get_all_location_with_dict()
        useraccount = Combine()
        return render_template("/users/create.html", form=useraccount, errors={}, locations=locations)
    else:
        useraccount = Combine()
        if useraccount.validate_on_submit():
            photopath = "/static/" + request.files["photo-photo"].filename
            hashedpassword = hasher.hash(useraccount.data["useraccount"]["password"])
            data = {"location": request.form["location"], "photo": photopath, "username": useraccount.data["useraccount"]['username'], "password": hashedpassword, "phoneNumber": useraccount.data["contactinfo"]["phoneNumber"], "email": useraccount.data["contactinfo"]["email"], "fax": useraccount.data["contactinfo"]["fax"], "homePhone": useraccount.data["contactinfo"]["homePhone"], "workmail": useraccount.data["contactinfo"]["workmail"], "lastEntry": datetime.datetime.now(), "joinedDate": datetime.datetime.now(), "securityAnswer": useraccount.data["useraccount"]["securityAnswer"], "membership": 0, "name": useraccount.data["person"]["name"], "surname": useraccount.data["person"]["surname"], "gender": useraccount.data["person"]["gender"], "birthday": useraccount.data["person"]["birthday"], "educationLevel": useraccount.data["person"]["educationLevel"], "facebook": useraccount.data["socialmedia"]["facebook"], "twitter": useraccount.data["socialmedia"]["twitter"], "instagram": useraccount.data["socialmedia"]["instagram"], "discord": useraccount.data["socialmedia"]["discord"], "youtube": useraccount.data["socialmedia"]["youtube"], "linkedin": useraccount.data["socialmedia"]["linkedin"]}
            if useraccount.data["useraccount"]["membershiptype"] == "Boss":
                data["membership"] = 1
            else:
                data["membership"] = 2
            response = create_user(data)
            if response[0]:
                request.files["photo-photo"].save("./static/" + request.files["photo-photo"].filename)
                session['username'] = data["username"]
                session['password'] = data["password"]
                session['membershiptype'] = 'Boss' if data['membership'] == 1 else 'Customer'
                session['userid'] = response[1]
                session['logged_in'] = True
            return redirect(url_for("users_page"))
        else:
            errs = []
            for fieldName, errorMessages in useraccount.errors.items():
                errs.append(errorMessages)
            errjson = json.dumps(errs)
            locations = get_all_location_with_dict()
            return render_template("/users/create.html", form=useraccount, errors=errjson, locations=locations)
        return render_template("/users/create.html", form=useraccount)

def signin_page():
    if request.method == "GET":
        return render_template("/users/login.html", alert="false")
    else:
        data = {"username": request.form['username'], "password": request.form["password"], "lastEntry": datetime.datetime.now()}
        userlist = select_users()
        for item in userlist :
            if item["username"] == data["username"] and hasher.verify(data["password"], item["password"]):
                session['username'] = data["username"]
                session['password'] = data["password"]
                session['userid'] = item["id"]
                session['logged_in'] = True
                session['membershiptype'] = 'Boss' if select_a_user(session['userid'])['membershiptype'] == 1 else 'Customer'
                update_user_lastentry(data, session["userid"])
                return redirect(url_for("home_page"))
    return render_template("/users/login.html", alert="true")
    
def profile_page():
    if request.method == "GET":
        user = select_a_user_and_info(session['userid'])
        return render_template("/users/profile.html", user=user[0]) 
    if request.method == 'POST':
        delete_current_user()
        session['username'] = ""
        session['password'] = ''
        session['logged_in'] = False
        session['membershiptype'] = ''
        
        return redirect(url_for("home_page"))
    
def logout_page():
    if request.method == "POST":
        session['membershiptype'] = ''
        session['username'] = ""
        session['password'] = ''
        session['userid'] = None
        session['logged_in'] = False
        return redirect(url_for("home_page"))


def editsocialmedia_page():
    if session == {} or session["logged_in"] == False:
        return redirect(url_for("home_page"))
    data = select_a_socialmedia(session['userid'])
    form = CallSocialMedia()
    if request.method == "POST" and form.validate_on_submit():
        socialdata = form.data["socialmedia"]
        update_socialmedia(socialdata, session["userid"])
        return redirect(url_for("profile_page"))
    elif request.method == "POST" and not form.validate_on_submit():
        errs = []
        for fieldName, errorMessages in form.errors.items():
            errs.append(errorMessages)
        errjson = json.dumps(errs)
        return render_template("/users/editsocialmedia.html", user=session, form=form, data = data, errors=errjson)
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
        if data["linkedin"] != None:
            form.socialmedia["linkedin"].data = data["linkedin"]
    return render_template("/users/editsocialmedia.html", user=session, form=form, data = data)  

def editcontactinfo_page():
    if session == {} or session["logged_in"] == False:
        return redirect(url_for("home_page"))
    data = select_a_contactinfo(session['userid'])
    form = CallContactInfo()
    if request.method == "POST" and form.validate_on_submit():
        contactinfodata = form.data["contactinfo"]
        contactinfodata["location"] = (request.form["location"])
        update_contactinfo(contactinfodata, session["userid"])
        return redirect(url_for("profile_page"))
    elif request.method == "POST" and not form.validate_on_submit():
        errs = []
        for fieldName, errorMessages in form.errors.items():
            #print(errorMessages)
            errs.append(errorMessages)
        errjson = json.dumps(errs)
        return render_template("/users/editcontactinfo.html", user=session, form=form, data = data, errors=errjson)
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
        locations = get_all_location_with_dict()
        return render_template("/users/editcontactinfo.html", user=session, form=form, data = data, locations=locations)  

def editperson_page():
    if session == {} or session["logged_in"] == False:
        return redirect(url_for("home_page"))
    data = select_a_person(session['userid'])
    form = CallPerson()
    if request.method == "POST" and form.validate_on_submit():
        persondata = form.data["person"]
        update_person(persondata, session["userid"])
        return redirect(url_for("profile_page"))
    elif request.method == "POST" and not form.validate_on_submit():
        errs = []
        for fieldName, errorMessages in form.errors.items():
            errs.append(errorMessages)
        errjson = json.dumps(errs)
        return render_template("/users/editperson.html", user=session, form=form, data = data, errors=errjson)
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
    data = select_a_user(session['userid'])
    form = CallUserAccount()
    if request.method == "POST" and form.validate_on_submit():
        userdata = form.data["user"]
        update_user(userdata, session["userid"])
        return redirect(url_for("profile_page"))
    elif request.method == "POST" and not form.validate_on_submit():
        errs = []
        for fieldName, errorMessages in form.errors.items():
            errs.append(errorMessages)
        errjson = json.dumps(errs)
        return render_template("/users/edituseraccount.html", user=session, form=form, data = data, errors=errjson)
    else:
        if data["username"] != None:
            form.user["username"].data = data["username"]
        if data["securityanswer"] != None:
            form.user["securityAnswer"].data = data["securityanswer"]
    return render_template("/users/edituseraccount.html", user=session, form=form, data = data)  