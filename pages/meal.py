from flask import Flask, render_template, request, redirect, url_for
import psycopg2 as dbapi2
import os
from models.meals import *
# DB_URL = os.getenv("DATABASE_URL")
DB_URL = "postgres://ivpallnyfezioy:075baf8e129b0d52dbd6d87dd3c774363b0b10b499921f821378ed7084bfc744@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dagmb1jla3rmdp"


def meal_page():
    ##Temprorary data
    user_type = 3
    is_Manager = False
    if user_type == 3:
        is_Manager=True
    else:
        is_Manager=False

    meals = ["Burger", "Fries", "Salad", "Drink", "Desert", "Side Meal"]

    if request.method == "GET":
        food_table = get_all_meals()
        return render_template("/meals/meals.html", mealss=meals, userType=is_Manager, f_table = food_table)
    else:
        search_dict = request.form.to_dict()
        if search_dict['searched_meal_name']:
            s_meal_name = search_dict['searched_meal_name']
            s_meal_name += "%"
        else:
            s_meal_name = search_dict['searched_meal_name']
            
        searched_meals = []
        for i in range(1, len(search_dict)):
            searched_meals.append(list(search_dict.keys())[i])

        

        connection=dbapi2.connect(DB_URL)
        cursor = connection.cursor()
        statement = "select food_id, food_name, brand_name, price, isVegan, type from food where food_name like %(meal_name)s"
        for s_m in searched_meals:
            statement += " or type='"+s_m+"'"
        statement += ";"
        cursor.execute(statement, {"meal_name": s_meal_name})
        food_table = cursor.fetchall()
        cursor.close()
        return render_template("/meals/meals.html", mealss=meals, userType=is_Manager, f_table = food_table)
    
def food_value_page(food_id):
    nutrition_table = get_food_value(food_id)
    return render_template("/meals/food_value.html", nutritions = nutrition_table, key=food_id)

def add_meal_page():
    mealTypes = ["Burger", "Fries", "Salad", "Drink", "Desert", "Side Meal"]
    if request.method == "GET":
        return render_template("/meals/add_meal.html", meal_types = mealTypes, food_props="")
    else:
        print("asdd")
        print(insert_meal(request.form))
        return redirect(url_for('meal_page')) 

def delete_meal_page(food_id):
    if request.method == "GET":
        food_name = select_name_by_id(food_id)
        return render_template("/meals/delete_meal.html", key = food_id, name=food_name)
    else:
        delete_meal(food_id)
        return redirect(url_for("meal_page"))

def update_meal_page(food_id):
    mealTypes = ["Burger", "Fries", "Salad", "Drink", "Desert", "Side Meal"]
    if request.method == "GET":
        food_properties, nutr_props = select_all_by_id(food_id) 
        print(nutr_props)
        return render_template("/meals/add_meal.html", key=food_id, food_props=food_properties, nutr_props = nutr_props, meal_types = mealTypes)
    else:
        update_meal(request.form, food_id)
        
        return redirect(url_for("meal_page"))

