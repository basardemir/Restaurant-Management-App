import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    "CREATE TABLE IF NOT EXISTS USERACCOUNT (id INTEGER PRIMARY KEY, lastEntry DATE, username VARCHAR(25), password VARCHAR(25), joinedDate DATE, securityAnswer VARCHAR(30))",
    "CREATE TABLE IF NOT EXISTS PERSON (id INTEGER PRIMARY KEY, name VARCHAR(50), surname VARCHAR(50), birthDay DATE, educationLevel VARCHAR(50), gender VARCHAR(20))",
    "CREATE TABLE IF NOT EXISTS CONTACTINFO (id INTEGER PRIMARY KEY, phoneNumber VARCHAR(20), email VARCHAR(30), fax VARCHAR(30), homePhone VARCHAR(50), contactType VARCHAR(50))",
    "CREATE TABLE IF NOT EXISTS MEMBERSHIP (id INTEGER PRIMARY KEY, membershipType VARCHAR (50))",
    "CREATE TABLE IF NOT EXISTS PHOTO (id INTEGER PRIMARY KEY, path VARCHAR (150))"

]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
