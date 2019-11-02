import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    "CREATE TABLE IF NOT EXISTS USERACCOUNT (id PRIMARY KEY INTEGER, lastEntry DATE, username VARCHAR(25), password VARCHAR(25), joinedDate DATE, securityAnswer VARCHAR(30))",
    "CREATE TABLE IF NOT EXISTS PERSON (id PRIMARY KEY INTEGER, name VARCHAR(50), surname VARCHAR(50), birthDay DATE, educationLevel VARCHAR(50), gender VARCHAR(20))",
    "CREATE TABLE IF NOT EXISTS CONTACTINFO (id PRIMARY KEY INTEGER, phoneNumber VARCHAR(20), email VARCHAR(30), fax VARCHAR(30), homePhone VARCHAR(50), contactType VARCHAR(50))",
    "CREATE TABLE IF NOT EXISTS MEMBERSHIP (id PRIMARY KEY INTEGER, membershipType VARCHAR (50))",
    "CREATE TABLE IF NOT EXISTS PHOTO (id PRIMARY KEY INTEGER, path VARCHAR (150))"
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
