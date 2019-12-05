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
    cursor.close()
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
            coordinates.longitude,
            timezone.timezone_id,
            coordinates.coord_id,
            properties.prop_id
            from (((country join properties on (country.properties=properties.prop_id))
            join timezone on (country.timezone=timezone.timezone_id))
            join coordinates on (country.capital_coordinates=coordinates.coord_id)) where country_id = %s;"""
            cursor.execute(query, (country_key,)) #expecting a tuple for second argument
            return (get_results(cursor))

def add_country(country):
    
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            query = """INSERT INTO PROPERTIES (AREA, GDP, POPULATION) VALUES (%s,%s,%s) RETURNING PROP_ID"""
            cursor.execute(query, (int(country[6]), float(country[7]*int(country[8])), float(country[9]*int(country[10]))))
            prop_id = cursor.fetchall()[0][0]
            connection.commit()
            #print(query % (int(country[6]), float(country[7]*int(country[8])), float(country[9]*int(country[10]))))
            #print(prop_id[0][0]) Prop_id is [(8,0)] a array of tuples with key at first value
            query = """INSERT INTO COORDINATES (LONGITUDE, LATITUDE) VALUES (%s,%s) RETURNING COORD_ID"""
            cursor.execute(query,(float(country[11]),float(country[12])))
            coord_id = cursor.fetchall()[0][0]
            connection.commit()
            query = """INSERT INTO COUNTRY
            (timezone,
            properties,
            capital_coordinates,
            name,
            country_code,
            driving_lane,
            capital_city,
            language_long,
            language_short) 
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING country_id"""
            #print(query % (22,prop_id,coord_id,country[0],country[1],country[2],country[3],country[4],country[5]))
            cursor.execute(query,(int(country[13]),prop_id,coord_id,country[0],country[1],country[2],country[3],country[4],country[5]))
            country_id = cursor.fetchall()[0][0]
            connection.commit()
            cursor.close()
    return country_id

def update_country(country):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            query = "UPDATE PROPERTIES SET AREA = %s, GDP= %s, POPULATION=%s WHERE prop_id = %s"
            cursor.execute(query, (country[9], country[10]*country[11],country[12]*country[13], country[2]))
            connection.commit()
            query = "UPDATE COORDINATES SET LONGITUDE=%s, LATITUDE=%s WHERE coord_id = %s"
            cursor.execute(query, (country[14],country[15],country[1]))
            connection.commit()
            query = """UPDATE COUNTRY SET
            timezone=%s,
            properties=%s,
            capital_coordinates=%s,
            name=%s,
            country_code=%s,
            driving_lane=%s,
            capital_city=%s,
            language_long=%s,
            language_short=%s 
            where country_id = %s"""
            cursor.execute(query, (country[16],country[2],country[1],country[3],country[4],country[5],country[6],country[7],country[8], country[0]))
            #print(query % (country[16],country[2],country[1],country[3],country[4],country[5],country[6],country[7],country[8], country[0]))
def delete_country(country_key):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            query = "DELETE FROM COUNTRY WHERE COUNTRY_ID = %s"
            try:
                cursor.execute(query, (country_key,))
            except:
                print("No country with given Id id found. No record was deleted.")
                cursor.close()
                return
            connection.commit()
            cursor.close()


def get_all_province():
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            query = """select
            country,
            province_id,
            country.name,
            province_name,
            properties.population,
            mayor,
            timezone.timezone,
            province_code
            from (((province join properties on (province.properties=properties.prop_id))
            join timezone on (province.timezone=timezone.timezone_id))
            join country on (country.country_id=province.country));
            """
            cursor.execute(query)
            return (get_results(cursor))
