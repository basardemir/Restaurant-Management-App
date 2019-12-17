from flask import Flask, render_template, request, redirect, url_for, session, abort

from .forms.country_form import ProvinceForm, refresh
from models.province_model import *

import psycopg2 as dbapi2  
from models.users import insert_contactinfo, update_contactinfo, select_a_user_and_info

def province_page():
    if request.method == "POST":
        for i in request.form.getlist("province_keys"):
            delete_province(i)

    province = get_all_province()
    count = get_count()
    return render_template("/province/index.html", list = province, count = count)

def province_add_page():
    #Session check needs to be implemented
    province = ProvinceForm()
    if province.validate_on_submit():
        province_info= (
            province.province["Country"].data,
            province.province["name"].data,
            province.province["mayor"].data,
            province.province["elevation"].data,
            province.province["province_code"].data,
            province.province["timezone"].data,
        )
        prop_info = (
            province.prop["Area"].data,
            province.prop["GDP"].data,
            province.prop["GDP_multiplier"].data,
            province.prop["Population"].data,
            province.prop["Population_multiplier"].data
        )
        #coord_info = (
        #    province.coord["Longitude"].data,
        #    province.coord["Latitude"].data,
        #)
        province_id = add_province(province_info, prop_info)
        return redirect(url_for('province_read_page', province_key = province_id))
        #return render_template("/province/create.html", form = province)
    return render_template("/province/create.html", form = province)

def province_read_page(province_key):
    result = get_province(province_key)
    if result is None:
        return abort(404)
    return render_template("/province/details.html", list = result)

def province_update_page(province_key):
    _province = get_province_all(province_key)
    province = ProvinceForm()

    if province.validate_on_submit():
        province_key = update_province(province, province_key, _province['prop_id'])
        return redirect(url_for('province_read_page', province_key=province_key))
    

    province.province["Country"].data               =_province['country']
    province.province["name"].data                  =_province['province_name']
    province.province["mayor"].data                 =_province['mayor']
    province.province["elevation"].data             =_province['avarage_elevation']
    province.province["province_code"].data         =_province['province_code']
    province.province["timezone"].data              =_province['timezone_id']
    province.prop["Area"].data                      =_province['area']
    province.prop["GDP"].data                       =_province['gdp']  /1000
    province.prop["GDP_multiplier"].data            ='1000' 
    province.prop["Population"].data                =_province['population'] / 1000
    province.prop["Population_multiplier"].data     ='1000'

    return render_template('/province/update.html', form = province)

def province_delete_page(province_key):
    delete_province(province_key)
    return redirect(url_for('province_page'))