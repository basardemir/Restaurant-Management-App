from flask import Flask, render_template


def meal_page():
    ##Temprorary data
    user_type = 3
    is_Manager = False
    if user_type == 3:
        is_Manager=True
    else:
        is_Manager=False
    ##Temprorary data
    meals = ["Burger", "Fries", "Salad", "Drink", "Desert", "Side Meal"]
    return render_template("/meals/meals.html", mealss=meals, userType=is_Manager)

def food_value_page():
    return render_template("/meals/food_value.html")

def add_meal_page():
    ##Temprorary data
    meals = ["Burger", "Fries", "Salad", "Drink", "Desert", "Side Meal"]
    return render_template("/meals/add_meal.html", meal_types = meals)