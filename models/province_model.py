from .db_prop import DB_URL, get_results
import psycopg2 as dbapi2

def get_count():
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("select count(*) from province")
            return(cursor.fetchone()[0])
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

def get_province(province_key):
    result = None
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            query = """
            select
            province_id,province_name,country.name, properties.population, properties.area, province_code, mayor, avarage_elevation, timezone.timezone, properties.gdp
            from (((province join properties on (province.properties=properties.prop_id))
            join timezone on (province.timezone=timezone.timezone_id))
            join country on (country.country_id=province.country)) where province_id = %s;
            """
            cursor.execute(query, (province_key,))
            desc = list(cursor.description[i][0] for i in range(0 ,len(cursor.description)))
            province = list(cursor.fetchone())
            result = dict(zip(desc, province))
            #print(desc)
            #print(province)  
            #print(result)
            return result  

def get_province_all(province_key):
    result = None
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            query = """
            select
            *
            from (((province join properties on (province.properties=properties.prop_id))
            join timezone on (province.timezone=timezone.timezone_id))
            join country on (country.country_id=province.country)) where province_id = %s;
            """
            cursor.execute(query, (province_key,))
            desc = list(cursor.description[i][0] for i in range(0 ,len(cursor.description)))
            province = list(cursor.fetchone())
            result = dict(zip(desc, province))
            #print(desc)
            #print(province)  
            #print(result)
            return result

def add_province(province, prop):
    province_id = -1
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            print(province)
            print(prop)
            query = """INSERT INTO PROPERTIES (AREA, GDP, POPULATION) VALUES (%s,%s,%s) RETURNING PROP_ID"""
            cursor.execute(query, (int(prop[0]), float(int(prop[1])*int(prop[2])), float(int(prop[3])*int(prop[4]))))
            prop_id = cursor.fetchall()[0][0]
            connection.commit()
            #query = """INSERT INTO COORDINATES (LONGITUDE, LATITUDE) VALUES (%s,%s) RETURNING COORD_ID"""
            #cursor.execute(query,(float(coord[0]),float(coord[1])))
            #coord_id = cursor.fetchall()[0][0]
            #connection.commit()
            query = """INSERT INTO PROVINCE
            (country,
            properties,
            timezone,
            province_name,
            mayor,
            avarage_elevation,
            province_code)
            VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING PROVINCE_ID
            """
            #print(query % (province[0],prop_id, province[5], province[1],province[2],province[3], province[4]))
            cursor.execute(query, (province[0],prop_id, province[5], province[1],province[2],province[3], province[4]))
            province_id = cursor.fetchall()[0][0]
            connection.commit()
    return province_id

def update_province(Incoming_form, province_id, prop_id ):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            query = """UPDATE PROPERTIES SET AREA = %s, GDP = %s, POPULATION=%s WHERE prop_id = %s"""
            #print(query % (int(Incoming_form.prop["Area"].data),int(Incoming_form.prop["GDP"].data)*int(Incoming_form.prop["GDP_multiplier"].data),int(Incoming_form.prop["Population"].data)*int(Incoming_form.prop["Population_multiplier"].data),prop_id))
            cursor.execute(query, (
            int(Incoming_form.prop["Area"].data),
            int(Incoming_form.prop["GDP"].data)*int(Incoming_form.prop["GDP_multiplier"].data),
            int(Incoming_form.prop["Population"].data)*int(Incoming_form.prop["Population_multiplier"].data), prop_id))
            connection.commit()
            
            query = """UPDATE PROVINCE SET province_name=%s, country=%s, province_code=%s,mayor=%s,avarage_elevation=%s,timezone=%s WHERE province_id=%s"""
            #print(query % (Incoming_form.province["name"].data,int(Incoming_form.province["Country"].data),int(Incoming_form.province["province_code"].data),Incoming_form.province["mayor"].data,int(Incoming_form.province["elevation"].data),int(Incoming_form.province["timezone"].data),province_id))
            cursor.execute(query, (Incoming_form.province["name"].data,
            int(Incoming_form.province["Country"].data),
            int(Incoming_form.province["province_code"].data),
            Incoming_form.province["mayor"].data,
            int(Incoming_form.province["elevation"].data),
            int(Incoming_form.province["timezone"].data),
            province_id))
            connection.commit()
    
    return province_id

    
def delete_province(province_key):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            #cursor.execute("select properties from province where province_id = %s", (province_key,))
            #DELETE FROM PROPERTIES WHERE PROP_ID = %s;
            #prop_key = cursor.fetchone()[0]
            #print(prop_key)
            query = """
            BEGIN TRANSACTION;
            DELETE FROM PROVINCE WHERE PROVINCE_ID = %s;
            COMMIT TRANSACTION;"""
            cursor.execute(query,(province_key,))
