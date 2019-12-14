from flask import Flask, render_template, request, redirect, url_for, session, abort

from .forms.country_form import LocationForm, refresh
from models.location_model import *

import psycopg2 as dbapi2  
from models.users import insert_contactinfo, update_contactinfo, select_a_user_and_info

def location_page():
    if request.method == "POST":
        for i in request.form.getlist("location_keys"):
            delete_location(i)

    location = get_all_location()
    print(location)
    return render_template("/location/index.html", list = location)

def location_add_page():
    location = LocationForm()
    if location.validate_on_submit():
        location_info = ( 
            int(location.location["province"].data),
            location.location["county"].data,
            location.location["neighborhood"].data,
            location.location["street"].data,
            location.location["zipcode"].data,
            location.location["description"].data
        )
        coord_info = (
            float(location.coord["Longitude"].data),
            float(location.coord["Latitude"].data)
        )
        location_id = add_location(location_info, coord_info)
        location = get_location(location_id)
        return render_template("/location/details.html", list = location)

    return render_template("/location/create.html", form = location)

def location_read_page(location_key):
    result = get_all_location()
    if result is None:
        return abort(404)
    return render_template("location/details.html", list = result)


def location_update_page(location_key):
    _location = get_location_all(location_key)
    location = LocationForm()

    if location.validate_on_submit():
        location_key = update_location(location, _location["location_id"], _location["coordinates"])
        return redirect(url_for('location_read_page', location_key=location_key))
    
    location.location["country"]            = _location['country'] 
    location.location["province"].data      = _location['province'] 
    location.location["county"].data        = _location['county'] 
    location.location["neighborhood"].data  = _location['neighborhood'] 
    location.location["street"].data        = _location['street'] 
    location.location["zipcode"].data       = _location['zipcode'] 
    location.location["description"].data   = _location['description'] 
    location.coord["Longitude"].data        = _location['longitude'] 
    location.coord["Latitude"].data         = _location['latitude']
     
    return render_template('/province/update.html', form = location)

def location_delete_page(location_key):
    delete_location(location_key)
    return redirect(url_for('location_page'))