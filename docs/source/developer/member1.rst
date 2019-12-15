Parts Implemented by İbrahim Berat Kaya
================================

Login
========

The user who has an account may sign in from this page using the username and password of the user. Once the user enters the account information, a request to the server will be made.  
If the user sends a valid form, the values of the form will be checked from the database. If a user exists, a session will be created for the user and the user will be logged in. 

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

Sign Up
========

The user who would like to join this application may create an account by entering the required information. Once the user enters the account information, they should click the sign up button. 
If the user enters a valid username that currently does not exists, they will join RestMang, and they will be redirected to the homepage. If the username is already taken, they will be alerted that the username is already taken.


   .. code-block:: python
        if check_if_user_exists(data) == False:
                photoid = insert_photo(data)
                id = insert_socialmedia(data)
                id = insert_contactinfo(data, id)
                id = insert_person(data, id, photoid)
                id = insert_useraccount(data, id)
                connection.commit()
                return [True, id]
