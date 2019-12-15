import psycopg2 as dbapi2
import os
DB_URL = "postgres://ivpallnyfezioy:075baf8e129b0d52dbd6d87dd3c774363b0b10b499921f821378ed7084bfc744@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dagmb1jla3rmdp"

def get_all_meals():
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "select food_id, food_name, brand_name, price, isVegan, type from food"
            cursor.execute(statement)
            food_table = cursor.fetchall()
            return food_table

def get_searched_meals(food_name, food_types):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            food_name += "%"
            statement = """select food_id, food_name, brand_name, 
                                    price, isVegan, type from food 
                                    where food_name like %(meal_name)s"""
            for ftype in food_types:
                statement += " or type='"+ftype+"'"
            statement += ";"
            cursor.execute(statement, {'meal_name': food_name})
            food_table = cursor.fetchall()
            return food_table

def get_food_value(food_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "select food_name, calories, carbohydrates, fat, protein, cholesterol from (nutritional_value join food on nutrition_id = nutritional_value_id) where food_id = %(food_id)s;"
            cursor.execute(statement, {'food_id': food_id})
            nutrition_talbe = cursor.fetchall()
            return nutrition_talbe

def insert_meal(meal_info):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "insert into FOOD (nutrition_id, food_name, brand_name, price, isVegan, type) VALUES (%(nutrition_id)s, %(food_name)s, %(brand_name)s, %(price)s, %(vegan)s, %(meal_option)s) RETURNING food_id;"
            statement2 = "insert into nutritional_value (protein, fat, carbohydrates, cholesterol, calories) values (%(protein)s, %(fat)s, %(carbohydrates)s, %(cholesterol)s, %(calories)s) RETURNING nutritional_value_id;"  
            cursor.execute(statement2, {'protein': meal_info['protein'], 'fat': meal_info['fat'], 'carbohydrates': meal_info['carbohydrates'], 'cholesterol': meal_info['cholesterol'],'calories': meal_info['calories']})
            connection.commit()
            nutrition_id = cursor.fetchone()[0]
            vegan = int(meal_info["VeganorNot"] == "Vegan")
            cursor.execute(statement, {'nutrition_id': nutrition_id, 'food_name': meal_info['meal_name'], 'brand_name': meal_info['brand_name'], 'price': meal_info['price'], 'vegan': vegan, 'meal_option': meal_info['meal_option']})
            connection.commit()
            food_id = cursor.fetchone()[0]
            stat = "insert into ingredients_for_food (food_id, ingredient_id, amount) values ( %(food_id)s, %(ingred_id)s, %(amount)s);"
            for i in range(1, 5):
                if meal_info['ingredient'+str(i)] != None and int(meal_info['Amount'+str(i)] != "") != 0:
                    cursor.execute(stat, {'food_id': food_id, 'ingred_id': meal_info['ingredient'+str(i)], 'amount': meal_info['Amount'+str(i)]})

            connection.commit()

            
            

            
            


def update_meal(new_props, food_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            
            statement = "update food set food_name=%(food_name)s, brand_name=%(brand_name)s, price=%(price)s, isVegan=%(isVegan)s, type=%(type)s where food_id = %(food_id)s;" 
            
            vegan = int(new_props['VeganorNot'] == "Vegan")
            
            cursor.execute(statement, {'food_name': new_props['meal_name'], 'brand_name': new_props['brand_name'], 'price':new_props['price'], 'isVegan':vegan, 'type':new_props['meal_option'], 'food_id':food_id})
            
            
            print(new_props)
            statement2 = "select nutrition_id from food where food_id = %(food_id)s"
            cursor.execute(statement2, {'food_id': food_id})
            nutrition_id = cursor.fetchone()[0]

            statement3 = "update nutritional_value set protein=%(protein)s, fat=%(fat)s, carbohydrates=%(carbohydrates)s, cholesterol=%(cholesterol)s, calories=%(calories)s where nutritional_value_id = %(nutrition_id)s;"
            
            cursor.execute(statement3, {'nutrition_id': nutrition_id, 'calories':  new_props['calories'], 'carbohydrates': new_props['carbohydrates'], 'fat': new_props['fat'], 'protein': new_props['protein'], 'cholesterol': new_props['cholesterol']})

            connection.commit()




def delete_meal(food_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            
            statement3 = "delete from ingredients_for_food where food_id=%(food_id)s;"
            cursor.execute(statement3, {'food_id': food_id})

            statement2 = "select nutrition_id from food where food_id = %(food_id)s"
            cursor.execute(statement2, {'food_id': food_id})
            nutrition_id = cursor.fetchone()[0]

            statement = "delete from food where food_id = %(food_id)s"
            cursor.execute(statement, {'food_id': food_id})

            statement3 = "delete from nutritional_value where nutritional_value_id = %(nutrition_id)s"
            cursor.execute(statement3, {'nutrition_id': nutrition_id})

            
            connection.commit()


def select_name_by_id(food_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "select food_name from food where food_id = %(food_id)s;"
            cursor.execute(statement, {'food_id': food_id})
            food_name = cursor.fetchone()[0]
            connection.commit()
            return food_name

def select_all_by_id(food_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "select nutrition_id, food_name, brand_name, price, isVegan, type from food where food_id = %(food_id)s;"
            statement2 = "select protein, fat, carbohydrates, cholesterol, calories from nutritional_value where nutritional_value_id = %(nutrition_id)s;"
            cursor.execute(statement, {'food_id': food_id})
            food_props = list(cursor.fetchall()[0])
            nutrition_id = food_props[0]
            food_props.pop(0)
            connection.commit()

            cursor.execute(statement2, {'nutrition_id': nutrition_id})
            nutr_props = list(cursor.fetchall()[0])
            connection.commit()


            return food_props, nutr_props


        
            
            






            



