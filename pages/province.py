from flask import Flask, render_template, request, redirect, url_for

import psycopg2 as dbapi2  
from .forms.country_form import CountryForm
from models.country import *

def province_page():
    province = get_all_province()
    print(province)
    return render_template("/province/index.html", list = province)

def province_add_page():
    return redirect(url_for('province_page'))

def province_read_page(province_key):
    return redirect(url_for('province_page'))

def province_update_page(province_key):
    return redirect(url_for('province_page'))

def province_delete_page(province_key):
    return redirect(url_for('province_page'))