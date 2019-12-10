import os
import psycopg2 as dbapi2
DB_URL = "postgres://ivpallnyfezioy:075baf8e129b0d52dbd6d87dd3c774363b0b10b499921f821378ed7084bfc744@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dagmb1jla3rmdp"


def add_ingredient(data):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement_photo = "insert into photo (path) values (%(img_path)s) returning id;"

            cursor.execute(statement_photo, {'img_path': data['photo_path']})

            photo_id = cursor.fetchone()[0]
            statement_nutr = "insert into nutritional_value (protein, fat, carbohydrates, cholesterol, calories) values (%(protein)s, %(fat)s, %(carbohydrates)s, %(cholesterol)s, %(calories)s) RETURNING nutritional_value_id;"
            
            cursor.execute(statement_nutr, {'protein': data['protein'], 'fat': data['fat'], 'carbohydrates': data['carbohydrates'], 'cholesterol': data['cholesterol'], 'calories': data['calories']})
            nutrition_id = cursor.fetchone()[0]
            
            statement_ing = "insert into ingredient (nutrition_id, photo_id, ingredient_name, ingredient_type, unit_weight, ingredient_volume, temperature_for_stowing) values (%(nutrition_id)s, %(photo_id)s, %(ingredient_name)s, %(ingredient_type)s, %(unit_weight)s, %(ingredient_volume)s, %(temperature_for_stowing)s);"
            cursor.execute(statement_ing, {'nutrition_id': nutrition_id, "photo_id": photo_id, 'ingredient_name': data['ingredient_name'], 'ingredient_type': data['ingredient_type'], 'unit_weight': data['unit_weight'], "ingredient_volume": data['volume'], "temperature_for_stowing": data['ideal_temp']})
            connection.commit()




