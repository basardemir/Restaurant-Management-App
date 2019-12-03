from flask import render_template
from datetime import datetime as dt

from pages.company import *
from pages.country import *
from pages.users import *
from pages.meal import *
from pages.card import *

def home_page():
  today = dt.today()
  day_name = today.strftime("%A")
  return render_template("home.html",day=day_name)

def not_found_page():
  return render_template("error-404.html")

def access_denied_page():
  return render_template("error-403.html")
