from flask import Flask, render_template, request, redirect, url_for, session, abort
from .forms.restaurant_form import Restaurant_Form, Restaurant_Page
from models.restaurant import *
import psycopg2 as dbapi2

def add_restaurant_page():
    _form = Restaurant_Page()
    if request.method == "GET":
        return render_template("/restaurant/add_restaurant.html", form = _form)
    else:
        print(request.form)
        rest_info = {"score": request.form['restaurant-score'], "capacity": request.form['restaurant-capacity'], "opening-date": request.form['restaurant-opening_date'], "manager": request.form['restaurant-manager'], "total_earning": request.form['restaurant-total_earning'], "company": request.form['company-company'], "contact": request.form['contact_info-contact']}
        add_restaurant(rest_info)
        return redirect(url_for('add_restaurant_page'))


def show_restaurant_page():
    restaurants = get_all_restaurants()
    return render_template("restaurant/read_restaurant.html", restaurants=restaurants, userType = session['membershiptype'])


def update_restaurant_page(restaurant_id):
    _form = Restaurant_Page()
    if request.method == "GET":
        restaurant = get_restaurant_by_id(restaurant_id)
        print(restaurant[0])
        _form.restaurant['score'].data = restaurant[2]
        _form.restaurant['capacity'].data = restaurant[3]
        _form.restaurant['opening_date'].data = restaurant[4]
        _form.restaurant['manager'].data = restaurant[5]
        _form.restaurant['total_earning'].data = restaurant[6]
        return render_template("restaurant/update_restaurant.html", form = _form)
    elif request.method == "POST":
        info = request.form
        update_restaurant_by_id(restaurant_id, info)
        return redirect(url_for('show_restaurant_page'))

def delete_restaurant_page(restaurant_id):
    if request.method == "GET":
        names = get_name_manager_by_id(restaurant_id)
        return render_template("/restaurant/delete_restaurant.html", data = names)
    else:
        delete_restaurant(restaurant_id)

def stock_page(restaurant_id):
    stock = stock_by_id(restaurant_id)
    return render_template("/restaurant/rest_details.html", stock=stock)



