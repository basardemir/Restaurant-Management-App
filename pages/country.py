from flask import Flask, render_template, request, redirect, url_for

import psycopg2 as dbapi2  ##temp for test purposes

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
	cursor = makeConnection()
	cursor.execute("select * from timezone")
	timezone = cursor.fetchall()
	cursor.close()
	if request.method =='GET':
		return render_template("/country/create.html", tz=timezone, value = None)
	else:
		#Form structure name,country code, diving lane, capital city, langugage long, langugage short, area, gdp, population, Longitude, latitude, timezone
		lon = request.form["lon"]
		lat = request.form["lat"]
		area = request.form["area"]
		gdp = request.form["gdp"]
		popu = request.form["population"]
		#country = {"name":None,"code":None,"lane":None,"capital":None,"Llong":None, "Lshort":None, "timezone":None}
		
		#country["name"] = request.form["name"]
		#country["code"] = request.form["code"]
		#country["lane"] = request.form["lane"]
		#country["capital"] = request.form["capital"]
		#country["Llong"] = request.form["Llong"]
		#country["Lshort"] = request.form["Lshort"]
		#country["timezone"] = request.form["timezone"]

		cursor = makeConnection()
		if lat != None and lon != None:
			cursor.execute("INSERT INTO COORDINATES (LONGITUDE, LATITUDE) VALUES (%s, %s)" % (lon, lat))
		cursor.execute("INSERT INTO PROPERTIES (AREA, GDP, POPULATION) VALUES (%s, %s, %s)" % (area, gdp, popu))
		cursor.close()
		return redirect(url_for("country_page")) #redirect to country_read_page for the latest entry

def country_read_page(country_key):
	##Country datastructure has to be pulled from the table using the key argument.
	country = None

	return render_template("country/read.html", country=country, key = country_key)

def country_update_page(country_key):
	
	return render_template("country/update.html", key=country_key)