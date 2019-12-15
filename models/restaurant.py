import psycopg2 as dbapi2
import os
DB_URL = "postgres://ivpallnyfezioy:075baf8e129b0d52dbd6d87dd3c774363b0b10b499921f821378ed7084bfc744@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dagmb1jla3rmdp"

def get_all_restaurants():
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "select restaurant_id, company.name, score, capacity, opening_date, manager, total_earning from (restaurant join company on company_belongs = company_id); "
            cursor.execute(statement)
            restaurant = cursor.fetchall()
            connection.commit()
            return restaurant

def add_restaurant(restaurant_info):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement3 = "insert into restaurant (company_belongs, contact_id, score, capacity, opening_date, manager, total_earning) values (%(company)s, %(contact)s,%(score)s, %(cap)s, %(date)s, %(manager)s, %(earning)s);"
            cursor.execute(statement3, {'company': restaurant_info['company'], 'contact': restaurant_info['contact'], 'score': restaurant_info['score'], 'cap': restaurant_info['capacity'], 'date': restaurant_info['opening-date'], 'manager': restaurant_info['manager'], 'earning': restaurant_info['total_earning']})
            connection.commit()

def get_restaurant_by_id(restaurant_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "select company_belongs, contact_id, score, capacity, opening_date, manager, total_earning from restaurant where restaurant_id = %(id)s;"
            cursor.execute(statement, {'id': restaurant_id})
            restaurant = cursor.fetchall()[0]
            print(restaurant)
            connection.commit()
            return restaurant

def update_restaurant_by_id(restaurant_id, info):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "update restaurant set company_belongs = %(company)s, contact_id=%(contact)s, score=%(score)s, capacity=%(cap)s, opening_date=%(date)s, manager=%(manager)s, total_earning=%(total)s where restaurant_id = %(id)s"
            cursor.execute(statement, {'company': int(info['company-company']), 'contact': info['contact_info-contact'], 'score': info['restaurant-score'], 'cap': info['restaurant-capacity'], 'date': info['restaurant-opening_date'], 'manager': info['restaurant-manager'], 'total': info['restaurant-total_earning'], 'id': restaurant_id})
            connection.commit()

def get_name_manager_by_id(restaurant_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "select company.name, manager from (restaurant join company on company_belongs=company_id) where restaurant_id = %(id)s;"
            cursor.execute(statement, {'id': restaurant_id})
            data = cursor.fetchall()
            connection.commit()
            return data
            
def delete_restaurant(restaurant_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:     
            statement1 = "delete from restaurant where restaurant_id = %(id)s;"
            statement2 = "delete from stock where restaurant_id = %(id)s;"
            cursor.execute(statement1, {'id': restaurant_id})
            cursor.execute(statement2, {'id': restaurant_id})

            connection.commit()

