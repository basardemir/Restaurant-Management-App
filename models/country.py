import os

online = False
if online:
    DB_URL = os.getenv("DATABASE_URL")
else:
    DB_URL = "postgres://ivpallnyfezioy:075baf8e129b0d52dbd6d87dd3c774363b0b10b499921f821378ed7084bfc744@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dagmb1jla3rmdp"

import psycopg2 as dbapi2

def get_results(cursor):
    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names,row)) for row in cursor.fetchall()] #array of dict
    #data[0].values() values of the first row
    res = []
    for i in data:
        res.append(i.values())
    print(i)
    return (res) #2d array 

def get_all_countries():
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            query = """select
            country_id,
            name,
            properties.population,
            properties.area,
            properties.gdp,
            timezone.timezone,
            language_short
            from (((country join properties on (country.properties=properties.prop_id))
            join timezone on (country.timezone=timezone.timezone_id))
            join coordinates on (country.capital_coordinates=coordinates.coord_id));"""
            cursor.execute(query)
            return (get_results(cursor))

def get_country(country_key):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            query = """select
            country_id,
            name,
            properties.population,
            properties.area,
            properties.gdp,
            timezone.timezone,
            language_short,
            language_long,
            country_code,
            driving_lane,
            capital_city,
            coordinates.latitude,
            coordinates.longitude
            from (((country join properties on (country.properties=properties.prop_id))
            join timezone on (country.timezone=timezone.timezone_id))
            join coordinates on (country.capital_coordinates=coordinates.coord_id));"""
            cursor.execute(query, country_key)
            return (get_results(cursor))

def add_country(country):
    print(country)

def update_country(country):
    print(country)

def delete_country(country):
    print(country)

