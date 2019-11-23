from flask import render_template
from datetime import datetime as dt

from pages.company import *
from pages.country import *
from pages.users import *
from pages.meal import *

def home_page():
  today = dt.today()
  day_name = today.strftime("%A")
  return render_template("home.html",day=day_name)

