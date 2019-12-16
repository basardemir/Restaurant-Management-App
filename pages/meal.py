from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2 as dbapi2
import os
from models.meals import *
from models.ingredients import *
from .forms.ingredient_form import Photo_Form
# DB_URL = os.getenv("DATABASE_URL")
DB_URL = "postgres://ivpallnyfezioy:075baf8e129b0d52dbd6d87dd3c774363b0b10b499921f821378ed7084bfc744@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dagmb1jla3rmdp"


def meal_page():
    food_table = get_all_meals()
    if request.method == "GET":
        print(food_table)
        return render_template("/meals/meals.html", userType=session['membershiptype'], f_table = food_table)
    else:
        print(request.form)
        orders = []
        for item in request.form:
            orders.append(item)
        return redirect(url_for('payment_page', meals=orders))
    
def food_value_page(food_id):
    nutrition_table, ingreds = get_food_value(food_id)
    return render_template("/meals/food_value.html", nutritions = nutrition_table, food_id=food_id, dictt = ingreds)

def add_meal_page():
    photo_form = Photo_Form()
    ingredients = get_names()
    if request.method == "GET":
        rests = get_brands()
        rest_dict = {}
        for item in reversed(rests):
            rest_dict[item[0]] = "Name:"+str(item[1])+", Manager:"+str(item[2])
        print(rest_dict)
        return render_template("/meals/add_meal.html", ingreds = ingredients, food_props="", nutr_props="", restaurant=rest_dict, form = photo_form)
    else:
        print(request.form)
        photo_path = "./static/" + request.files["photo"].filename
        insert_meal(request.form, photo_path)
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

