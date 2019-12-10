from flask import Flask, render_template, request, redirect, url_for, session, abort
from models.ingredients import *
from .forms.ingredient_form import Ingredient_Page

def add_ingredient_page():
    _form = Ingredient_Page()
    if request.method == "GET":
        return render_template("/ingredients/add_ingd.html", form = _form)
    else:
        if _form.validate_on_submit():
            photo_path = "./static/" + request.files["photo-photo"].filename
            data = {"ingredient_name" : request.form['ingredient-ingred_name'], "ingredient_type": request.form['ingredient-ingred_type'], "unit_weight": request.form['ingredient-unit_weight'], "volume": request.form['ingredient-volume'], "ideal_temp": request.form['ingredient-ideal_temp'], "protein": request.form['nutrition-protein'], "carbohydrates": request.form['nutrition-carbohydrates'], "fat": request.form["nutrition-fat"], "cholesterol": request.form['nutrition-cholesterol'], "calories": request.form['nutrition-calories'], "photo_path": photo_path}
            add_ingredient(data)
            request.files["photo-photo"].save("./static/" + request.files["photo-photo"].filename)
            return render_template("/meals/meals.html")
    


    