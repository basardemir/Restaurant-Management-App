from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms_components import IntegerField
from wtforms.fields.html5 import DateTimeLocalField

from datetime import datetime


msg = "The column must be filled."


class CompanyForm(FlaskForm):
  name            = StringField("Name", validators = [ DataRequired(message = msg) ])
  information     = TextAreaField("Information", validators = [ DataRequired(message = msg) ])
  mission         = TextAreaField("Mission", validators = [ DataRequired(message = msg) ])
  vision          = TextAreaField("Vision",  validators = [ DataRequired(message = msg) ])
  abbrevation     = StringField("Abbrevation",  validators = [ DataRequired(message = msg) ])
  foundation_date = DateTimeLocalField('Founded Date', format='%Y-%m-%dT%H:%M')
  type            = SelectField("Type", choices=[ ('-1', 'Choose one!'), ('LTD', 'Limited'), ('AS', 'Anonim')])

