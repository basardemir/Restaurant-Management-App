from flask import render_template

from pages.company import *
from pages.country import *
from pages.users import *

def home_page():
  return render_template("home.html")