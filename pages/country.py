from flask import Flask, render_template, request, redirect, url_for


def country_page():
	if request.method == 'GET':
		##get all the countries from the table
		#########TEST DATA#########
		countryList = [[1,"Turkey"], [2,"USA"], [3,"Combodia"]]
		return render_template("/country/details.html", countries = countryList)
	else:
		form_country_keys = request.form.getlist("country_keys")
		for country_key in form_country_keys:
			print("Country with the key: " + country_key + " is deleted")
			#delete country with the given key
		return redirect(url_for("country_page"))
	

def country_add_page():
	if request.method =='GET':
		#input restriction parameters will be set here and send with render template
		return render_template("/country/create.html")
	else:
		print("add page post")
		form_name = request.form["name"] #country name
		#generate a valid table entry using the parameters send from the form
		#add entry to db table
		key = 0 #lastest entry key will be assigned here
		return redirect(url_for("country_page")) #redirect to country_read_page for the latest entry


def country_read_page(country_key):
	##Country datastructure has to be pulled from the table using the key argument.
	country = None

	return render_template("country/read.html", country=country, key = country_key)

def country_update_page(country_key):
	
	return render_template("country/update.html", key=country_key)
