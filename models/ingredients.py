import os
import psycopg2 as dbapi2
DB_URL = os.getenv("DATABASE_URL")


def add_ingredient(data):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement_photo = "insert into photo (path) values (%(img_path)s) returning id;"

            cursor.execute(statement_photo, {'img_path': data['photo_path']})

            photo_id = cursor.fetchone()[0]
            statement_nutr = "insert into nutritional_value (protein, fat, carbohydrates, cholesterol, calories) values (%(protein)s, %(fat)s, %(carbohydrates)s, %(cholesterol)s, %(calories)s) RETURNING nutritional_value_id;"
            
            cursor.execute(statement_nutr, {'protein': data['protein'], 'fat': data['fat'], 'carbohydrates': data['carbohydrates'], 'cholesterol': data['cholesterol'], 'calories': data['calories']})
            nutrition_id = cursor.fetchone()[0]
            
            statement_ing = "insert into ingredient (nutrition_id, photo_id, ingredient_name, ingredient_type, unit_weight, ingredient_volume, temperature_for_stowing) values (%(nutrition_id)s, %(photo_id)s, %(ingredient_name)s, %(ingredient_type)s, %(unit_weight)s, %(ingredient_volume)s, %(temperature_for_stowing)s) returning ingredient_id;"
            cursor.execute(statement_ing, {'nutrition_id': nutrition_id, "photo_id": photo_id, 'ingredient_name': data['ingredient_name'], 'ingredient_type': data['ingredient_type'], 'unit_weight': data['unit_weight'], "ingredient_volume": data['volume'], "temperature_for_stowing": data['ideal_temp']})
            ingredient_id = cursor.fetchone()[0]
            print(data['expire_date'])
            statement_stock = "insert into stock (ingredient_id, restaurant_id, expire_date, stock_left) values (%(ing_id)s, %(rest_id)s, %(date)s, %(stock)s);"
            cursor.execute(statement_stock, {'ing_id': ingredient_id, 'rest_id': data['rest_id'], 'stock': data['stock'], 'date': data['expire_date']})
            connection.commit()


def show_all_ingredients():
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "select ingredient_id, path, ingredient_name, ingredient_type, unit_weight, ingredient_volume, temperature_for_stowing from (photo inner join ingredient on photo_id = id);"
            cursor.execute(statement)
            ingred_table = cursor.fetchall()
            connection.commit()
            return ingred_table

def get_nutr_values(ingred_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "select ingredient_name, calories, carbohydrates, fat, protein, cholesterol from (nutritional_value join ingredient on nutrition_id = nutritional_value_id) where ingredient_id = %(ingred_id)s;"
            cursor.execute(statement, {'ingred_id': ingred_id})
            nutrition_table = cursor.fetchall()
            return nutrition_table

def select_ingred_name_by_id(ingred_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "select ingredient_name from ingredient where ingredient_id = %(ingred_id)s; "
            cursor.execute(statement, {'ingred_id': ingred_id})
            ingred_name = cursor.fetchone()[0]
            connection.commit()
            return ingred_name

def delete_ingred(ingred_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "select photo_id, nutrition_id from ingredient where (ingredient_id = %(ingred_id)s);"
            cursor.execute(statement, {'ingred_id': ingred_id})

            photo_id, nutrition_id = cursor.fetchone()
            
            statement5 = "delete from stock where ingredient_id = %(id)s;"
            cursor.execute(statement5, {'id': ingred_id})

            statementt6 = "delete from ingredients_for_food where ingredient_id = %(id)s;"
            cursor.execute(statementt6, {'id': ingred_id})

            statement4 = "delete from ingredient where ingredient_id=%(id)s;"
            cursor.execute(statement4, {'id': ingred_id})

            statement2 = "delete from photo where id = %(photo_id)s;"
            cursor.execute(statement2, {'photo_id': photo_id})

            statement3 = "delete from nutritional_value where(nutritional_value_id = %(nutr_id)s);"
            cursor.execute(statement3, {'nutr_id': nutrition_id})

            connection.commit()

def update_ingred(new_props, ingred_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            print(new_props['ingredient-ingred_name'])
            statement = "update ingredient set ingredient_name=%(ingred_name)s, ingredient_type=%(ingred_type)s, unit_weight=%(weight)s, ingredient_volume=%(volume)s, temperature_for_stowing=%(temp)s where ingredient_id = %(ingred_id)s;"
            cursor.execute(statement, {'ingred_name': new_props['ingredient-ingred_name'], 'ingred_type':new_props['ingredient-ingred_type'], 'weight':new_props['ingredient-unit_weight'], 'volume':new_props['ingredient-volume'], 'temp':new_props['ingredient-ideal_temp'], 'ingred_id': ingred_id})
            connection.commit()

def get_ingredient_by_id(ingred_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "select ingredient_name, ingredient_type, unit_weight, ingredient_volume, temperature_for_stowing from ingredient where ingredient_id = %(ingred_id)s;"
            cursor.execute(statement, {'ingred_id': ingred_id})
            ingredient = cursor.fetchall()[0]
            return ingredient

def get_names():
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "select ingredient_name, ingredient_id from ingredient;"
            cursor.execute(statement)
            names = cursor.fetchall()
            connection.commit()
            return names






