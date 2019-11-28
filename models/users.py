import os
DB_URL = os.getenv("DATABASE_URL")

import psycopg2 as dbapi2


def insert_socialmedia(data):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "INSERT INTO SOCIALMEDIA (facebook, twitter, instagram, discord, youtube, googleplus) VALUES (%s, %s, %s, %s, %s, %s);"
            cursor.execute(statement, (data["facebook"], data['twitter'], data["instagram"], data["discord"], data["youtube"], data["googleplus"]))
            connection.commit()
    
def insert_contactinfo(data):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "INSERT INTO CONTACTINFO (socialmedia, phoneNumber, email, fax, homePhone, workmail) VALUES ((SELECT SOCIALMEDIA.id FROM SOCIALMEDIA WHERE (facebook=%s and twitter=%s and instagram=%s and discord=%s and youtube=%s and googleplus=%s)), %s, %s, %s, %s, %s);"
            cursor.execute(statement, (data["facebook"], data['twitter'], data["instagram"], data["discord"], data["youtube"], data["googleplus"], data['phoneNumber'], data["email"], data["fax"], data["homePhone"], data["workmail"]))
            connection.commit()
    
def insert_person(data):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "INSERT INTO PERSON (contactinfo, name, surname, birthDay, educationLevel, gender) VALUES ((SELECT CONTACTINFO.id FROM CONTACTINFO WHERE (phoneNumber=%s and email=%s and fax=%s and homePhone=%s and workmail=%s)), %s, %s, %s, %s, %s);"
            cursor.execute(statement, (data['phoneNumber'], data["email"], data["fax"], data["homePhone"], data["workmail"], data["name"], data['surname'], data["birthday"], data["education"], data["gender"]))
            connection.commit()
    
def insert_useraccount(data):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "INSERT INTO USERACCOUNT (person, lastEntry, username, password, joinedDate, securityAnswer, membershiptype) VALUES ((SELECT PERSON.id FROM PERSON WHERE (name=%s and surname=%s and birthDay=%s and educationLevel=%s and gender=%s)), %s, %s, %s, %s, %s, %s);"
            cursor.execute(statement, (data["name"], data['surname'], data["birthday"], data["education"], data["gender"], data["lastEntry"], data['username'], data["password"], data["joinedDate"], data["securityAnswer"], data["membership"]))
            connection.commit()

def create_user(data):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            insert_contactinfo(data)
            insert_socialmedia(data)
            insert_person(data)
            insert_useraccount(data)
            connection.commit()
            print("User created")
        