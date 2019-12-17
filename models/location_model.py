from .db_prop import DB_URL, get_results
import psycopg2 as dbapi2

def get_all_location_with_dict():
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            query = """select 
            location_id,
            country.country_id,
            country.name,
            province.province_id,
            province.province_name,
            county,
            neighborhood,
            street,
            zipcode,
            description from 
            ((location join province on (location.province = province.province_id))
            join country on (province.country = country.country_id))
            """
            cursor.execute(query)
            connection.commit()
            res = cursor.fetchall()
            return res

def get_all_location():
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            query = """select 
            location_id,
            country.country_id,
            country.name,
            province.province_id,
            province.province_name,
            county,
            neighborhood,
            street,
            zipcode,
            description from 
            ((location join province on (location.province = province.province_id))
            join country on (province.country = country.country_id))
            """
            cursor.execute(query)
            #desc = list(cursor.description[i][0] for i in range(0 ,len(cursor.description)))
            #province = list(cursor.fetchone())
            #result = dict(zip(desc, province))
            #print(result)
            return get_results(cursor)

def get_location(location_key):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            query = """select 
            location_id,
            country.country_id,
            country.name,
            province.province_id,
            province.province_name,
            county,
            neighborhood,
            street,
            zipcode,
            description from 
            ((location join province on (location.province = province.province_id))
            join country on (province.country = country.country_id)) where location_id = %s
            """
            cursor.execute(query, (location_key,))
            #desc = list(cursor.description[i][0] for i in range(0 ,len(cursor.description)))
            #province = list(cursor.fetchone())
            #result = dict(zip(desc, province))
            #print(result)
            return get_results(cursor)

def add_location(location, coord):
    
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            query = """INSERT INTO COORDINATES (LONGITUDE, LATITUDE) VALUES (%s,%s) RETURNING COORD_ID"""
            cursor.execute(query,(coord[0], coord[1]))
            retCoord = cursor.fetchone()[0]
            query = """INSERT INTO LOCATION 
            (province,
            coordinates,
            county,
            neighborhood,
            street,
            zipcode,
            description
            ) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING LOCATION_ID"""
            cursor.execute(query, (location[0],retCoord,location[1],location[2],location[3],location[4],location[5]))
            retLoc = cursor.fetchone()[0]
    return retLoc

def get_location_all(location_key):
    result = None
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            query = """select 
            *
            from ((location join province on ((location.province = province.province_id))
            join country on (province.country = country.country_id)) join coordinates on (location.coordinates = coordinates.coord_id))
            where location_id = 7;
            """
            cursor.execute(query, (location_key,))
            desc = list(cursor.description[i][0] for i in range(0 ,len(cursor.description)))
            
            location = list(cursor.fetchone())
            result = dict(zip(desc, location))
            return result

def update_location(Incoming_location, location_id, coordinate_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            query = """UPDATE LOCATION SET province=%s, county=%s, neighborhood=%s, street=%s, zipcode=%s, description=%s where location_id = %s """
            cursor.execute(query, (
                int(Incoming_location.location["province"]),
                Incoming_location.location["county"],
                Incoming_location.location["neighborhood"],
                Incoming_location.location["street"],
                Incoming_location.location["zipcode"],
                Incoming_location.location["description"],
                location_id)
                )
            connection.commit()
            query = """UPDATE COORDINATES SET LONGITUDE=%s, LATITUDE=%s where coor_id=%s"""
            cursor.execute(query, float((Incoming_location.coord["Longitude"].data), float(Incoming_location.coord["Latitude"].data)), coordinate_id)
            connection.commit()

    return  location_id


def delete_location(location_key):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            query = """
            BEGIN TRANSACTION;
            DELETE FROM location WHERE location_id = %s;
            COMMIT TRANSACTION;
            """
            cursor.execute(query, (location_key,))
            connection.commit()
        