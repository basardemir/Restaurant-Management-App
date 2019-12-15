from flask import Flask, render_template, request, redirect, url_for, session, abort
from models.ingredients import *
from .forms.ingredient_form import Ingredient_Page, Ingredient_Form, Ing_with_Button

def add_ingredient_page():
    _form = Ingredient_Page()
    if request.method == "GET":
        return render_template("/ingredients/add_ingd.html", form = _form)
    else:
        print(request.form)
        photo_path = "./static/" + request.files["photo-photo"].filename
        data = {"ingredient_name" : request.form['ingredient-ingred_name'], "ingredient_type": request.form['ingredient-ingred_type'], "unit_weight": request.form['ingredient-unit_weight'], "volume": request.form['ingredient-volume'], "ideal_temp": request.form['ingredient-ideal_temp'], "protein": request.form['nutrition-protein'], "carbohydrates": request.form['nutrition-carbohydrates'], "fat": request.form["nutrition-fat"], "cholesterol": request.form['nutrition-cholesterol'], "calories": request.form['nutrition-calories'], "photo_path": photo_path, "rest_id": request.form['restaurant-restaurant'], 'stock': request.form['restaurant-stock'], 'expire_date': request.form['restaurant-expire_date']}
        add_ingredient(data)
        request.files["photo-photo"].save("./static/" + request.files["photo-photo"].filename)
        return redirect(url_for('show_ingredients'))

def show_ingredients():
    ing_table = show_all_ingredients()
    return render_template("/ingredients/read_ingd.html", ing_table = ing_table, userType = 1)

def ingredient_nutr_values(ingred_id):
    table = get_nutr_values(ingred_id)
    return render_template("ingredients/ingred_value.html", nutritions = table)

def delete_ingredient_page(ingred_id):
    if request.method == "GET":
        name = select_ingred_name_by_id(ingred_id)
        return render_template("ingredients/delete_ingred.html", name = name)
    else:
        delete_ingred(ingred_id) 
        return redirect(url_for('show_ingredients'))

def update_ingredient_page(ingred_id):
    _form = Ing_with_Button()
    
    if request.method == "GET":
        ingred = get_ingredient_by_id(ingred_id)

        _form.ingredient['ingred_name'].data = ingred[0]
        _form.ingredient['ingred_type'].data = ingred[1]
        _form.ingredient['unit_weight'].data = ingred[2]
        _form.ingredient['volume'].data = ingred[3]
        _form.ingredient['ideal_temp'].data = ingred[4]
        
        return render_template("/ingredients/update_ingred.html", form=_form)
   
    else:
        update_ingred(request.form, ingred_id)
        return redirect(url_for('show_ingredients'))

    


    