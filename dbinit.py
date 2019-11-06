import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    "CREATE TABLE IF NOT EXISTS USERACCOUNT (id INTEGER PRIMARY KEY, lastEntry DATE, username VARCHAR(25), password VARCHAR(25), joinedDate DATE, securityAnswer VARCHAR(30))",
    "CREATE TABLE IF NOT EXISTS PERSON (id INTEGER PRIMARY KEY, name VARCHAR(50), surname VARCHAR(50), birthDay DATE, educationLevel VARCHAR(50), gender VARCHAR(20))",
    "CREATE TABLE IF NOT EXISTS CONTACTINFO (id INTEGER PRIMARY KEY, phoneNumber VARCHAR(20), email VARCHAR(30), fax VARCHAR(30), homePhone VARCHAR(50), contactType VARCHAR(50))",
    "CREATE TABLE IF NOT EXISTS MEMBERSHIP (id INTEGER PRIMARY KEY, membershipType VARCHAR (50))",
    "CREATE TABLE IF NOT EXISTS PHOTO (id INTEGER PRIMARY KEY, path VARCHAR (150))",
	"""CREATE TABLE IF NOT EXISTS LOCATION(
			LOCATION_ID SERIAL PRIMARY KEY,
			PROVINCE INTEGER,
			COORDINATES INTEGER,
			COUNTY VARCHAR(40),
			NEIGHBORHOOD VARCHAR(40),
			STREET VARCHAR(40),
			ZIPCODE VARCHAR(5),
			DESCRIPTION VARCHAR(100),
			FOREIGN KEY (IL) REFERENCES PROVINCE(PROVINCE_ID),
			FOREIGN KEY (COORDINATES) REFERENCES COORDINATES(COORD_ID)
	);
	""",
    """CREATE TABLE IF NOT EXISTS COUNTRY(
			COUNTRY_ID SERIAL PRIMARY KEY,
			TIMEZONE INTEGER,
			PROPERTIES INTEGER,
			CAPITAL_COORDINATES INTEGER,
			COUNTRY_CODE VARCHAR(2),
			REGION VARCHAR(20),
			DRIVING_LANE VARCHAR(5),
			LANGUAGE_SHORT VARCHAR(3),
			LANGUAGE_LONG VARCHAR(15),
			FOREIGN KEY (TIMEZONE) REFERENCES TIMEZONE(TIMEZONE_ID),
			FOREIGN KEY (CAPITAL_COORDINATES) REFERENCES COORDINATES(COORD_ID),
			FOREIGN KEY (PROPERTIES) REFERENCES PROPERTIES(PROP_ID)
		);
  	""",
    """CREATE TABLE IF NOT EXISTS PROVINCE(
			PROVINCE_ID SERIAL PRIMARY KEY,
			COUNTRY INTEGER,
			PROPERTIES INTEGER,
			TIMEZONE INTEGER,
			PROVINCE_NAME VARCHAR(40),
			CITY_CODE VARCHAR(5),
			AVARAGE_ELEVATION NUMERIC,
			SHORT_NAME VARCHAR(5),
			FOREIGN KEY (COUNTRY) REFERENCES COUNTRY(COUNTRY_ID),
			FOREIGN KEY (PROPERTIES) REFERENCES PROPERTIES(PROP_ID),
			FOREIGN KEY (TIMEZONE) REFERENCES TIMEZONE(TIMEZONE_ID)
		);
	""",
	"""CREATE TABLE IF NOT EXISTS PROPERTIES(
			PROP_ID SERIAL PRIMARY KEY,
			AREA NUMERIC,
			POPULATION INTEGER,
			GDP NUMERIC
		); 
	""",
	"""CREATE TABLE IF NOT EXISTS COORDINATES(
			COORD_ID SERIAL PRIMARY KEY,
			LONGITUDE NUMERIC,
			LATITUDE NUMERIC
		);
	""",
	"""CREATE TABLE IF NOT EXISTS TIMEZONE(
			TIMEZONE_ID SERIAL PRIMARY KEY,
			TIMEZONE VARCHAR(10)
		);
	""",
	"""CREATE TABLE IF NOT EXISTS _comment(
		id serial primary key,
		description varchar(150),
		score numeric(3,1),
		up_vote int default 0,
		down_vote int default 0,
		created_at TIMESTAMP default CURRENT_TIMESTAMP,

		user_id int,
		order_id int,

		check ((score >= 1.0) and (score <= 10.0))
	);""",

	"""CREATE TABLE IF NOT EXISTS _card(
		id serial primary key,

		points int,
		card_number char(16) unique,
		is_active smallint,
		color varchar(20),
		activation_date TIMESTAMP default CURRENT_TIMESTAMP,
		expire_date TIMESTAMP default (CURRENT_TIMESTAMP+interval'1 year'),

		user_id int,
		company_id int
	);""",

	"""CREATE TABLE IF NOT EXISTS _company(
		id serial primary key,
		name varchar(50),
		information varchar(1000),
		mission varchar(1000),
		vision varchar(1000),
		abbrevation varchar(10),
		foundation_date TIMESTAMP,

		type varchar(10), -- LTD, 
		user_id int, -- Founder info
		contact_id int -- company contact_info
	);""",

	"""CREATE TABLE IF NOT EXISTS _order(
		id serial primary key,
		price float,
		note varchar(500),
		type varchar(11), -- cash or credit card
		created_at TIMESTAMP default CURRENT_TIMESTAMP, -- order date
		end_at TIMESTAMP, -- ending order date.

		restaurant_id int,
		customer_id int,
		employee_id int,
	  	card_id int -- for speacial card of company.
	);""",

	"""CREATE TABLE IF NOT EXISTS _orderfoods(
		order_id int,
		food_id int,
	  	amount int not null,
	  	primary key(order_id, food_id)
	);""",

	"""CREATE TABLE IF NOT EXISTS _employee(
		id serial primary key,

		restaurant_id int,
		user_id int -- it covers that Employee and Manager via MembershipType
	);""",
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
