import os
DB_URL = "postgres://ivpallnyfezioy:075baf8e129b0d52dbd6d87dd3c774363b0b10b499921f821378ed7084bfc744@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dagmb1jla3rmdp"	#os.getenv("DATABASE_URL")
from flask import session
import psycopg2 as dbapi2
import psycopg2.extras


#Gets data from the photo table when given the photo_id
def get_photo_with_id(photo_id): 
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            statement = "SELECT * FROM PHOTO WHERE id=%s;"
            cursor.execute(statement, (photo_id, ))
            connection.commit()
            photolist = cursor.fetchall()
            return photolist

#Updates data from the photo table when given the photo_id
def update_photo_with_id(photo_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            id = select_a_contactinfo(userid)["id"]
            statement = "UPDATE PHOTO SET path=%s WHERE id=%s"
            cursor.execute(statement, (path, photo_id))
            connection.commit()

#inserts into the photo table when given the dictionary data with attribute photo which contains the image path
def insert_photo(data):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "INSERT INTO PHOTO (path) VALUES (%s) RETURNING id;"
            cursor.execute(statement, (data["photo"], ))
            connection.commit()
            id = cursor.fetchone()[0]
            return id

#Deletes a photo row from the photo table when given the id
def delete_a_photo(id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "DELETE FROM PHOTO WHERE id = %s"
            cursor.execute(statement, (id, ))
            connection.commit()


#Gets data from the contactinfo table when given the contactinfo_id
def get_contactinfo_with_id(contactinfo_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            statement = "SELECT * FROM CONTACTINFO WHERE id=%s;"
            cursor.execute(statement, (contactinfo_id, ))
            connection.commit()
            contactinfolist = cursor.fetchall()
            return contactinfolist

#Updates data from the contactinfo table when given the contactinfo_id
def update_contactinfo_with_id(contactinfo_id, data):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            id = select_a_contactinfo(userid)["id"]
            statemenryt = "UPDATE CONTACTINFO SET phoneNumber=%s, email=%s, fax=%s, homePhone=%s, workmail=%s WHERE id=%s"
            cursor.execute(statement, (data["phoneNumber"], data["email"], data["fax"], data["homePhone"], data["workmail"], contactinfo_id))
            connection.commit()

#Insert into the socialmedia table with the data dictionary
def insert_socialmedia(data):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "INSERT INTO SOCIALMEDIA (facebook, twitter, instagram, discord, youtube, googleplus) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"
            cursor.execute(statement, (data["facebook"], data['twitter'], data["instagram"], data["discord"], data["youtube"], data["googleplus"]))
            connection.commit()
            id = cursor.fetchone()[0]
            return id
    
#Insert into the contactinfo table with the data dictionary, and the desired socialmedia_id
def insert_contactinfo(data, socialmedia_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "INSERT INTO CONTACTINFO (socialmedia, phoneNumber, email, fax, homePhone, workmail) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"
            cursor.execute(statement, (socialmedia_id, data['phoneNumber'], data["email"], data["fax"], data["homePhone"], data["workmail"]))
            connection.commit()
            id = cursor.fetchone()[0]
            return id

#Delete a row from the contactinfo table with the id
def delete_a_contactinfo(id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "DELETE FROM CONTACTINFO WHERE id = %s"
            cursor.execute(statement, (id, ))
            connection.commit()

#Delete a row from the socialmedia table with the id
def delete_a_socialmedia(id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "DELETE FROM SOCIALMEDIA WHERE id = %s"
            cursor.execute(statement, (id, ))
            connection.commit()

def get_user_by_username(username):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "SELECT * FROM USERACCOUNT WHERE username = %s;"
            cursor.execute(statement, (username, ))
            connection.commit()
            userlist = list( cursor.fetchone() )
            desc = list( cursor.description[i][0] for i in range(0, len(cursor.description)) )
            res = dict(zip(desc, userlist ))
            return res

def check_if_user_exists(data):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "SELECT * FROM USERACCOUNT WHERE username=%s;"
            cursor.execute(statement, (data["username"], ))
            connection.commit()
            userlist = cursor.fetchall()
            if userlist == []:
                return False
            else:
                return True


def select_users():
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            statement = "SELECT * FROM USERACCOUNT"
            cursor.execute(statement)
            connection.commit()
            data = cursor.fetchall()
            return data

def select_users_membership_and_photo():
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            statement = "SELECT * FROM (SELECT * FROM USERACCOUNT JOIN MEMBERSHIP ON MEMBERSHIP.id = USERACCOUNT.membershiptype) AS USERANDMEMBER FULL OUTER JOIN (SELECT PHOTO.path, PERSON.id FROM PHOTO JOIN PERSON ON PERSON.photo = PHOTO.id) AS T1 ON T1.id = USERANDMEMBER.person"
            cursor.execute(statement)
            connection.commit()
            data = cursor.fetchall()
            return data

def select_person():
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "SELECT * FROM PERSON"
            cursor.execute(statement)
            connection.commit()
            data = cursor.fetchall()
            return data

def select_all_users_and_info():
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            statement = "SELECT * FROM SOCIALMEDIA JOIN (SELECT * FROM CONTACTINFO JOIN (SELECT * FROM (SELECT PERSON.id, contactinfo, name, surname, birthday, educationLevel, gender, path FROM PERSON JOIN PHOTO ON PHOTO.id = PERSON.photo) AS PER JOIN (SELECT * FROM USERACCOUNT JOIN MEMBERSHIP ON USERACCOUNT.membershiptype = MEMBERSHIP.id) AS T2 ON PER.id = T2.person) AS T3 ON CONTACTINFO.id = T3.contactinfo) AS T4 ON T4.socialmedia = SOCIALMEDIA.id;"
            cursor.execute(statement)
            connection.commit()
            userlist = cursor.fetchall()
            cursor.close()
            return userlist
    
def select_a_user_and_info(userid):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            statement = "SELECT * FROM SOCIALMEDIA JOIN (SELECT * FROM CONTACTINFO JOIN (SELECT * FROM (SELECT PERSON.id, contactinfo, name, surname, birthday, educationLevel, gender, path FROM PERSON JOIN PHOTO ON PHOTO.id = PERSON.photo) AS PER JOIN ((SELECT * FROM USERACCOUNT WHERE id = %s) AS T JOIN MEMBERSHIP ON T.membershiptype = MEMBERSHIP.id) AS T2 ON PER.id = T2.person) AS T3 ON CONTACTINFO.id = T3.contactinfo) AS T4 ON T4.socialmedia = SOCIALMEDIA.id;"
            cursor.execute(statement, (userid, ))
            connection.commit()
            userlist = cursor.fetchall()
            cursor.close()
            return userlist
    


def check_if_photo_exists(data):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "SELECT * FROM PHOTO WHERE (path=%s);"
            cursor.execute(statement, (data["photo"], ))
            connection.commit()
            photolist = cursor.fetchall()
            if photolist == []:
                return False
            else:
                return True

    
def insert_person(data, contactinfo_id, photo_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "INSERT INTO PERSON (contactinfo, photo, name, surname, birthDay, educationLevel, gender) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;"
            cursor.execute(statement, (contactinfo_id, photo_id, data["name"], data['surname'], data["birthday"], data["educationLevel"], data["gender"]))
            connection.commit()
            id = cursor.fetchone()[0]
            return id
    
    
def insert_useraccount(data, person_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "INSERT INTO USERACCOUNT (person, lastEntry, username, password, joinedDate, securityAnswer, membershiptype) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;"
            cursor.execute(statement, (person_id, data["lastEntry"], data['username'], data["password"], data["joinedDate"], data["securityAnswer"], data["membership"]))
            connection.commit()
            id = cursor.fetchone()[0]
            return id

def create_user(data):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            if check_if_user_exists(data) == False:
                photoid = insert_photo(data)
                id = insert_socialmedia(data)
                id = insert_contactinfo(data, id)
                id = insert_person(data, id, photoid)
                id = insert_useraccount(data, id)
                connection.commit()
                return [True, id]
            else:
                return [False, -1]

def select_socialmedia():
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            statement = "SELECT * FROM SOCIALMEDIA;"
            cursor.execute(statement)
            connection.commit()
            data = cursor.fetchall()
            return data

def select_a_socialmedia(userid):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            statement = "SELECT * FROM SOCIALMEDIA JOIN (SELECT socialmedia FROM CONTACTINFO JOIN (SELECT contactinfo FROM PERSON JOIN ((SELECT person FROM USERACCOUNT WHERE id=%s)) AS T2 ON PERSON.id = T2.person) AS T3 ON T3.contactinfo = CONTACTINFO.id) AS T4 ON T4.socialmedia = SOCIALMEDIA.id;"
            cursor.execute(statement, (userid, ))
            connection.commit()
            data = cursor.fetchall()
            return data[0]

def select_a_photo(userid):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            statement = "SELECT * FROM PHOTO JOIN (SELECT photo FROM PERSON JOIN (SELECT person FROM USERACCOUNT WHERE id = %s) AS T2 ON T2.person = PERSON.id) AS T1 ON T1.photo = PHOTO.id;"
            cursor.execute(statement, (userid, ))
            connection.commit()
            data = cursor.fetchall()
            return data[0]

def update_socialmedia(data, userid):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            id = select_a_socialmedia(userid)["id"]
            statement = "UPDATE SOCIALMEDIA SET facebook=%s, twitter=%s, instagram=%s, discord=%s, youtube=%s, googleplus=%s WHERE id=%s"
            cursor.execute(statement, (data["facebook"], data["twitter"], data["instagram"], data["discord"], data["youtube"], data["googleplus"], id))
            connection.commit()


def select_a_contactinfo(userid):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            statement = "SELECT * FROM CONTACTINFO JOIN (SELECT contactinfo FROM PERSON JOIN ((SELECT person FROM USERACCOUNT WHERE id=%s)) AS T2 ON PERSON.id = T2.person) AS T3 ON T3.contactinfo = CONTACTINFO.id"
            cursor.execute(statement, (userid, ))
            connection.commit()
            data = cursor.fetchall()
            return data[0]

def update_contactinfo(data, userid):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            id = select_a_contactinfo(userid)["id"]
            statement = "UPDATE CONTACTINFO SET phoneNumber=%s, email=%s, fax=%s, homePhone=%s, workmail=%s WHERE id=%s"
            cursor.execute(statement, (data["phoneNumber"], data["email"], data["fax"], data["homePhone"], data["workmail"], id))
            connection.commit()


def select_a_person(userid):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            statement = "SELECT * FROM PERSON JOIN (SELECT person FROM USERACCOUNT WHERE id=%s) AS T2 ON PERSON.id = T2.person;"
            cursor.execute(statement, (userid, ))
            connection.commit()
            data = cursor.fetchall()
            return data[0]

def update_person(data, userid):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            id = select_a_person(userid)["id"]
            statement = "UPDATE PERSON SET name=%s, surname=%s, birthday=%s, educationLevel=%s, gender=%s WHERE id=%s"
            cursor.execute(statement, (data["name"], data["surname"], data["birthday"], data["educationLevel"], data["gender"], id))
            connection.commit()


def select_a_user(userid):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            statement = "SELECT * FROM USERACCOUNT WHERE id=%s;" 
            cursor.execute(statement, (userid, ))
            connection.commit()
            data = cursor.fetchall()
            return data[0]

def update_user(data, userid):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            statement = "UPDATE USERACCOUNT SET username=%s, password=%s, securityAnswer=%s WHERE id=%s"
            cursor.execute(statement, (data["username"], data["password"], data["securityAnswer"], userid))
            session["username"] = data["username"]
            session["password"] = data["password"]
            connection.commit()

def update_user_lastentry(data, userid):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            statement = "UPDATE USERACCOUNT SET lastEntry=%s WHERE id=%s"
            cursor.execute(statement, (data["lastEntry"], userid))
            connection.commit()


def delete_a_person(id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "DELETE FROM PERSON WHERE id = %s"
            cursor.execute(statement, (id, ))
            connection.commit()
            



def delete_a_user(id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "DELETE FROM USERACCOUNT WHERE id = %s"
            cursor.execute(statement, (id, ))
            connection.commit()

def delete_current_user():
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            id = select_a_user(session['userid'])["id"]
            person_id = select_a_person(session['userid'])["id"]
            photo_id = select_a_photo(session['userid'])["id"]
            contactinfo_id = select_a_contactinfo(session['userid'])["id"]
            socialmedia_id = select_a_socialmedia(session['userid'])["id"]
            if(photo_id != None):
                delete_a_photo(photo_id)
            if(socialmedia_id != None):
                delete_a_socialmedia(socialmedia_id)
            if(contactinfo_id != None):
                delete_a_contactinfo(contactinfo_id)
            if(person_id != None):
                delete_a_person(person_id)
            if(id != None):
                delete_a_user(id)

            