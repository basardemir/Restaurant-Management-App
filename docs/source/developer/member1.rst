Parts Implemented by İbrahim Berat Kaya
================================

Useraccount Table
------------

The Useraccount Table consists of 5 non-key fields about the account information of the user such as a username, a password, a joined date, a last entry date, and a security question answer. The Useraccount Table has a foreign key to the Membership Table to store the membership type of the user, and a foreign key to the Person Table to store personal information of the user. 


Person Table
-------------

The Person Table consists of 5 non-key fields. The fields are the name of the user, the surname of the user, birthday of the user, education level of the user, and gender of the user. The Person Table has a foreign key to the Photo Table to store the path of the user profile image, and a foreign key to the Contactinfo Table to store contact information. 


Contactinfo Table
-------------

The Contactinfo Table consists of 5 non-key fields. The fields are the phone number of the user, the email of the user, fax of the user, home phone number of the user, and work mail of the user. The Contactinfo Table has a foreign key to the Location Table to store the location information of the user, and a foreign key to the Socialmedia Table to store the social media links of the user. 


Socialmedia Table
-------------

The Socialmedia Table consists of 6 non-key fields. The fields are the Facebook link of the user, Twitter link of the user, Instagram link of the user, Discord link of the user, YouTube link of the user, LinkedIn link of the user.


Photo Table
------------

The Photo Table consists of a 1 non-key field. The Photo Table stores the path of the image uploaded to the server.


Membership Table
------------

The Membership Table consists of a 1 non-key field. The Membership Table stores the membership type of the user where the values can be an admin, a customer, or a boss.


Login
-----------

The user who has an account may sign in from this page using the username and password of the user. Once the user enters the account information, a request to the server will be made.  
If the user sends a valid form, the values of the form will be checked from the database. If a user exists, a session will be created for the user and the user will be logged in. 

SQL Query:

   .. code-block:: python

    def select_users():
        with dbapi2.connect(DB_URL) as connection:
            with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                statement = "SELECT * FROM USERACCOUNT"
                cursor.execute(statement)
                connection.commit()
                data = cursor.fetchall()
                return data

HTML Form:

    .. code-block:: html

    <form id="form" class="container-fluid w-75" action="" method="post" name="{{url_for('add_user_page')}}">
        <h1 class="text-center">Login</h1>
        <div class="field-group">
            <label style="font-weight: bold; margin-top: 0.75rem;" for="username" class="label">Username</label>
            <input type="text" name="username" class="form-control" required="required" />
            <label style="font-weight: bold; margin-top: 0.75rem;" for="password" class="label">Password</label>
            <input type="password" name="password" class="form-control" required="required" />
        </div>
        <div id="buttondiv" class="field is-grouped text-center" style="margin-top: 1rem;">
            <div class="control">
                <button id="button" class="btn btn-outline-info">Sign in</button>
            </div>
        </div>
    </form>


Python Code:

   .. code-block:: python

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

Signup
-----------

The user who would like to join this application may create an account by entering the required information. Once the user enters the account information, they should click the sign up button. 
If the user enters a valid username that currently does not exists, they will join RestMang, and they will be redirected to the homepage. If the username is already taken, they will be alerted that the username is already taken.

SQL Query:

   .. code-block:: python

        def create_user(data):
            with dbapi2.connect(DB_URL) as connection:
                with connection.cursor() as cursor:
                    if check_if_user_exists(data) == False:
                        photoid = insert_photo(data)  #Each insert function is an insert query
                        id = insert_socialmedia(data)
                        id = insert_contactinfo(data, id)
                        id = insert_person(data, id, photoid)
                        id = insert_useraccount(data, id)
                        connection.commit()
                        return [True, id]
                    else:
                        return [False, -1]


Insert function:

   .. code-block:: python

        def insert_socialmedia(data):
            with dbapi2.connect(DB_URL) as connection:
                with connection.cursor() as cursor:
                    statement = "INSERT INTO SOCIALMEDIA (facebook, twitter, instagram, discord, youtube, linkedin) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"
                    cursor.execute(statement, (data["facebook"], data['twitter'], data["instagram"], data["discord"], data["youtube"], data["linkedin"]))
                    connection.commit()
                    id = cursor.fetchone()[0]
                    return id

WTForm:

   .. code-block:: python

    class Combine(FlaskForm):
        person = FormField(PersonForm)
        useraccount = FormField(UserAccountForm)
        contactinfo = FormField(ContactInfoForm)
        socialmedia = FormField(SocialMedia)
        photo = FormField(PhotoForm)
        submit = SubmitField("Sign Up", render_kw={"class": "btn btn-outline-info"})



Python Code:

   .. code-block:: python
   
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
            errs = [["Username is already taken"]]
            errjson = json.dumps(errs)
            return render_template("/users/create.html", form=useraccount, errors=errjson, locations=locations)


Profile
-----------

The user who has an existing user account may access information from their user account once they view the profile page while logged in. Once the user goes to the profile page, the information about the user will be retrieved from the database. The information will then be shown to the user.


SQL Query:

   .. code-block:: python

        def select_a_user_and_info(userid):
            with dbapi2.connect(DB_URL) as connection:
                with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                    statement = """SELECT * FROM (select location_id,country.country_id,country.name as country_name,province.province_id,province.province_name,county,neighborhood,street,zipcode, description from 
                    ((location join province on (location.province = province.province_id))
                    join country on (province.country = country.country_id))) AS T6 JOIN (SELECT * FROM SOCIALMEDIA JOIN 
                    (SELECT * FROM CONTACTINFO JOIN (SELECT * FROM (SELECT PERSON.id, contactinfo, name, surname, birthday, educationLevel, gender, path FROM PERSON JOIN PHOTO ON PHOTO.id = PERSON.photo) AS PER JOIN 
                    ((SELECT * FROM USERACCOUNT WHERE id = %s) AS T JOIN MEMBERSHIP ON T.membershiptype = MEMBERSHIP.id) AS T2 ON PER.id = T2.person) AS T3 ON CONTACTINFO.id = T3.contactinfo) AS T4 ON T4.socialmedia = SOCIALMEDIA.id)
                    AS T5 ON T5.location=T6.location_id;"""
                    cursor.execute(statement, (userid, ))
                    connection.commit()
                    userlist = cursor.fetchall()
                    cursor.close()
                    return userlist


Python Code:

   .. code-block:: python
   
        if request.method == "GET":
            user = select_a_user_and_info(session['userid'])
            return render_template("/users/profile.html", user=user[0]) 

Editing 
-----------

The user may edit the current information about their account, personal information, contact information, and social media information. The user is redirected to the form of the table they desire to edit. The user may change the desired field they would like to change. Once the form is submitted, the data sent will be used to update the database of the updated table.


SQL Query:

   .. code-block:: python

        def select_a_user(userid):
            with dbapi2.connect(DB_URL) as connection:
                with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
                    statement = "SELECT * FROM USERACCOUNT WHERE id=%s;" 
                    cursor.execute(statement, (userid, ))
                    connection.commit()
                    data = cursor.fetchall()
                    return data[0]


WTForm:

   .. code-block:: python

    class UserEditAccountForm(FlaskForm):
        username = StringField("Username", validators=[DataRequired(message = msg),Length(max=25, message="Username cannot be longer than 25 characters")], render_kw={"class": "form-control"})
        password = PasswordField("Password", validators=[DataRequired(message=msg), Length(max=25, message="Password cannot be longer than 25 characters")], render_kw={"class": "form-control"})
        securityAnswer = StringField("Security Answer", validators=[Length(max=30, message="Security answer cannot be longer than 30 characters")], render_kw={"class": "form-control", "placeholder": "What is your mother's maiden name?"})

    class CallUserAccount(FlaskForm):
        user = FormField(UserEditAccountForm)
        submit = SubmitField("Update", render_kw={"class": "btn btn-outline-info"})


Python Code:

   .. code-block:: python

        #One of the editing pages
        def edituser_page():
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