import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS PHOTO (
        id SERIAL PRIMARY KEY, 
        path VARCHAR(150)
    );""",
    """CREATE TABLE IF NOT EXISTS SOCIALMEDIA(
        id SERIAL PRIMARY KEY,
        facebook VARCHAR(60),
        twitter VARCHAR(60),
        instagram VARCHAR(60),
        discord VARCHAR(60),
        youtube VARCHAR(60),
        linkedin VARCHAR(60)
    );""",
		"""CREATE TABLE IF NOT EXISTS TIMEZONE(
			TIMEZONE_ID SERIAL PRIMARY KEY,
			TIMEZONE VARCHAR(10)
		);
     	""",
	"""CREATE TABLE IF NOT EXISTS COORDINATES(
			COORD_ID SERIAL PRIMARY KEY,
			LONGITUDE NUMERIC,
			LATITUDE NUMERIC
		);
	""",
	"""CREATE TABLE IF NOT EXISTS PROPERTIES(
			PROP_ID SERIAL PRIMARY KEY,
			AREA NUMERIC,
			POPULATION INTEGER,
			GDP NUMERIC
		); 
	""",
    """CREATE TABLE IF NOT EXISTS MEMBERSHIP (
        id SERIAL PRIMARY KEY, 
        membershipType VARCHAR(50)
    );""",
		

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
	"""CREATE TABLE IF NOT EXISTS LOCATION(
			LOCATION_ID SERIAL PRIMARY KEY,
			PROVINCE INTEGER,
			COORDINATES INTEGER,
			COUNTY VARCHAR(40),
			NEIGHBORHOOD VARCHAR(40),
			STREET VARCHAR(40),
			ZIPCODE VARCHAR(5),
			DESCRIPTION VARCHAR(100),
			FOREIGN KEY (PROVINCE) REFERENCES PROVINCE(PROVINCE_ID),
			FOREIGN KEY (COORDINATES) REFERENCES COORDINATES(COORD_ID)
	);
	""",
    """CREATE TABLE IF NOT EXISTS CONTACTINFO (
        id SERIAL PRIMARY KEY, 
        socialmedia INTEGER,
        location INTEGER,
        phoneNumber VARCHAR(20), 
        email VARCHAR(30), 
        fax VARCHAR(30), 
        homePhone VARCHAR(50), 
        workmail VARCHAR(50),
        FOREIGN KEY (socialmedia) REFERENCES SOCIALMEDIA(id) on delete set null,
        FOREIGN KEY (location) REFERENCES LOCATION(LOCATION_ID) on delete set null
    );""",
    """CREATE TABLE IF NOT EXISTS PERSON (
        id SERIAL PRIMARY KEY, 
        contactinfo INTEGER,
        photo INTEGER,
        name VARCHAR(50), 
        surname VARCHAR(50), 
        birthDay DATE, 
        educationLevel VARCHAR(50), 
        gender VARCHAR(20),
        FOREIGN KEY (contactinfo) REFERENCES CONTACTINFO(id) on delete set null,
        FOREIGN KEY (photo) REFERENCES PHOTO(id) on delete set null
    );""",
		"""CREATE TABLE IF NOT EXISTS USERACCOUNT (
        id SERIAL PRIMARY KEY, 
        person INTEGER,
        membershiptype INTEGER,
        lastEntry DATE, 
        username VARCHAR(25), 
        password VARCHAR(100), 
        joinedDate DATE, 
        securityAnswer VARCHAR(30),
        FOREIGN KEY (person) REFERENCES PERSON(id) on delete set null,
        FOREIGN KEY (membershiptype) REFERENCES MEMBERSHIP(id) on delete set null
    );""",
    
	
	
	"""CREATE TABLE IF NOT EXISTS COMPANY(
	COMPANY_ID SERIAL PRIMARY KEY,
	NAME VARCHAR(50),
	INFORMATION VARCHAR(1000),
	MISSION VARCHAR(1000),
	VISION VARCHAR(1000),
	ABBREVATION VARCHAR(10),
	FOUNDATION_DATE TIMESTAMP,
	TYPE VARCHAR(10), -- LTD, 
	USER_ID INT, -- FOUNDER INFO
	CONTACT_ID INT, -- COMPANY CONTACT_INFO

	FOREIGN KEY (USER_ID) REFERENCES USERACCOUNT(id) ON DELETE SET NULL,
	FOREIGN KEY (CONTACT_ID) REFERENCES CONTACTINFO(id) ON DELETE CASCADE
	);
	""",
	"""
	CREATE TABLE IF NOT EXISTS CARD(
		CARD_ID SERIAL PRIMARY KEY,

		POINTS INT,
		CARD_NUMBER CHAR(16) UNIQUE,
		IS_ACTIVE SMALLINT,
		COLOR VARCHAR(20),
		ACTIVATION_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		EXPIRE_DATE TIMESTAMP DEFAULT (CURRENT_TIMESTAMP+INTERVAL'1 YEAR'),

		USER_ID INT,
		COMPANY_ID INT,
		
		FOREIGN KEY (USER_ID) REFERENCES USERACCOUNT(id) ON DELETE CASCADE,
		FOREIGN KEY (COMPANY_ID) REFERENCES COMPANY(COMPANY_ID) ON DELETE CASCADE
	);
	""",
	
	"""CREATE TABLE IF NOT EXISTS restaurant(
		restaurant_id serial primary key,
		company_belongs INTEGER,
		contact_id INTEGER,
		score INTEGER,
		capacity INTEGER NOT NULL,
		opening_date DATE,
		manager VARCHAR(100),
		total_earning INTEGER,
		FOREIGN KEY (company_belongs) REFERENCES COMPANY(COMPANY_ID) ON DELETE CASCADE,
		FOREIGN KEY (contact_id) REFERENCES CONTACTINFO(id),
		CHECK ((score >= 1) AND (score <= 5))
	);""",

	"""
	CREATE TABLE IF NOT EXISTS ORDERS(
		ORDER_ID SERIAL PRIMARY KEY,
		PRICE FLOAT,
		NOTE VARCHAR(500),
		TYPE VARCHAR(11), -- CASH OR CREDIT CARD
		RATE INT,
		CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- ORDER DATE
		END_AT TIMESTAMP, -- ENDING ORDER DATE.
		
		RESTAURANT_ID INT,
		USER_ID INT,
		FOREIGN KEY (RESTAURANT_ID) REFERENCES RESTAURANT(RESTAURANT_ID) ON DELETE SET NULL,
		FOREIGN KEY (USER_ID) REFERENCES USERACCOUNT(id) ON DELETE SET NULL
	);
	""",
	"""
	CREATE TABLE IF NOT EXISTS COMMENT(
		COMMENT_ID SERIAL PRIMARY KEY,
		TITLE VARCHAR(50),
		DESCRIPTION VARCHAR(300),
		CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		SPEED SMALLINT,
		TASTE SMALLINT,
		USER_ID INT,
		ORDER_ID INT,
		FOREIGN KEY (USER_ID) REFERENCES USERACCOUNT(id) ON DELETE CASCADE,
		FOREIGN KEY (ORDER_ID) REFERENCES ORDERS(ORDER_ID) ON DELETE CASCADE
	);
	""",

	"""CREATE TABLE IF NOT EXISTS nutritional_value(
		nutritional_value_id serial primary key,
		protein FLOAT,
		fat FLOAT,
		carbohydrates FLOAT,
		cholesterol FLOAT,
		calories FLOAT
	);""",

	"""CREATE TABLE IF NOT EXISTS FOOD(
		food_id serial primary key,
		photo_id INTEGER,
		nutrition_id INTEGER,
		food_name VARCHAR(100) UNIQUE NOT NULL,
		brand_name VARCHAR(100) NOT NULL,
		price INTEGER,
		isVegan INTEGER not null,
		FOREIGN KEY (photo_id) REFERENCES PHOTO(id),
		FOREIGN KEY (nutrition_id) REFERENCES nutritional_value(nutritional_value_id)
	);""",

	"""
	CREATE TABLE IF NOT EXISTS ORDER_FOOD(
		ORDER_ID INT,
		FOOD_ID INT,
		AMOUNT INT NOT NULL,
		PRIMARY KEY(ORDER_ID, FOOD_ID),
		
		FOREIGN KEY (ORDER_ID) REFERENCES ORDERS(ORDER_ID) ON DELETE CASCADE,
		FOREIGN KEY (FOOD_ID) REFERENCES FOOD(FOOD_ID) ON DELETE SET NULL
	);
	""",

	"""CREATE TABLE IF NOT EXISTS ingredient(
		ingredient_id serial primary key,
		nutrition_id INTEGER,
		photo_id INTEGER,
		ingredient_name VARCHAR(100) UNIQUE NOT NULL,
		ingredient_type INTEGER NOT NULL,
		unit_weight INTEGER,
		ingredient_volume INTEGER,
		temperature_for_stowing INTEGER,
		FOREIGN KEY (nutrition_id) REFERENCES nutritional_value(nutritional_value_id),
		FOREIGN KEY (photo_id) REFERENCES PHOTO(id),
		CHECK ((temperature_for_stowing >= 0))
	);""",

	"""CREATE TABLE IF NOT EXISTS STOCK(
		ingredient_id INTEGER,
		restaurant_id INTEGER,
		expire_date DATE,
		stock_left INTEGER,
		primary key(ingredient_id, restaurant_id),
		FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id),
		FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id)

	);""",

	"""CREATE TABLE IF NOT EXISTS ingredients_for_food(
		food_id INTEGER,
		ingredient_id INTEGER,
		amount FLOAT not null,
		primary key (food_id, ingredient_id),
		FOREIGN KEY (food_id) REFERENCES FOOD(food_id),
		FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)
	);"""

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
