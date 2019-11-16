from flask import render_template
import datetime

from pages.company import *
from pages.country import *
from pages.users import *

def home_page():
  today = datetime.today()
  day_name = today.strftime("%A")
  return render_template("home.html", day = day_name)