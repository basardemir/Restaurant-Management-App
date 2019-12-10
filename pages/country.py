from flask import Flask, render_template, request, redirect, url_for

import psycopg2 as dbapi2  
from .forms.country_form import CountryForm
from models.country_model import *
url="postgres://ivpallnyfezioy:075baf8e129b0d52dbd6d87dd3c774363b0b10b499921f821378ed7084bfc744@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dagmb1jla3rmdp"

def makeConnection():
	connection=dbapi2.connect(url)
	cursor=connection.cursor()
	return cursor

def tz_page():
	cursor = makeConnection()
	cursor.execute("select * from timezone")
	timezone = cursor.fetchall()
	cursor.close()
	return render_template("/timezone/index.html", list = timezone)

def country_page():
	if request.method == "POST":
		for i in request.form.getlist("country_keys"):
			delete_country(i)
	
	country = get_all_countries()
	return render_template("/country/details.html", countries = country)
	
def country_add_page():
	country = CountryForm()

	if country.validate_on_submit():
		print("Validated")
		country_info = (
			country.data["name"],
			country.data["short_code"],
			country.data["lane"],
			country.data["Capital_City"],
			country.data["Language_Long"],
			country.data["Language_Short"],
			country.data["Area"],
			country.data["GDP"],
			country.data["GDP_multiplier"],
			country.data["Population"],
			country.data["Population_multiplier"],
			country.data["Longitude"],
			country.data["Latitude"],
			country.data["timezone"]
		)
		key = add_country(country_info)
		country = get_country(key) 
		return redirect(url_for("country_read_page",country_key=key))
	
	return render_template("/country/create.html", form=country)

def country_read_page(country_key):
	country = get_country(country_key)
	return render_template("country/read.html", country=country, key = country_key)

def country_update_page(country_key):
	_country = get_country(country_key)
	form = CountryForm()
	
	if form.validate_on_submit():
		country_info = (
				list(_country[0])[0], #Country_id print(list(_country[0])[0])
				list(_country[0])[14], #coord_id
				list(_country[0])[15], #prop_id
				
				form.data["name"],	#country[3]
				form.data["short_code"],
				form.data["lane"],
				form.data["Capital_City"],
				form.data["Language_Long"],
				form.data["Language_Short"],
				int(form.data["Area"]),	#country[9]
				float(form.data["GDP"]),
				int(form.data["GDP_multiplier"]),
				float(form.data["Population"]),
				int(form.data["Population_multiplier"]),
				float(form.data["Longitude"]), #country[14]
				float(form.data["Latitude"]),
				int(form.data["timezone"])
			)
		
		update_country(country_info)
		return redirect(url_for("country_read_page", country_key = country_key ))

	for key,name,pop,area,gdp,tz,ls,ll,cc,dl,cc2,lat,lon,tz_id,cr_id,pr_id in _country:
		print(key,name,pop,area,gdp,tz,ls,ll,cc,dl,cc2,lat,lon)
		form.name.data = name
		form.short_code.data = cc
		form.lane.data = dl
		form.Capital_City.data = cc2
		form.Language_Long.data = ll
		form.Language_Short.data = ls
		form.Area.data = area
		form.GDP.data = gdp / 1000
		form.GDP_multiplier.data = "1000"
		form.Population.data = pop / 1000
		form.Population_multiplier.data = "1000"
		form.Longitude.data = lon
		form.Latitude.data = lat
		form.timezone.data = str(tz_id)
		
	return render_template("country/update.html", form=form)

def country_delete_page(country_key):
	delete_country(country_key)
	return(redirect(url_for("country_page")))