from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, ValidationError
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms_components import IntegerField
from wtforms.fields.html5 import DateTimeLocalField

from datetime import datetime

msgRequired = "The column must be filled."
msgChosen   = "Must choose one of them."

typeChoices = [
  ('-1', 'Choose one!'), 
  ('LTD', 'Limited'), 
  ('AS', 'Anonim')
]

def unselectedValid(form, field):
  if field.data == "-1":
    raise ValidationError(msgChosen)    
  

class CompanyForm(FlaskForm):
  
  name            = StringField("Name", validators = [ DataRequired(message = msgRequired) ])
  information     = TextAreaField("Information", validators = [ DataRequired(message = msgRequired) ])
  mission         = TextAreaField("Mission", validators = [ DataRequired(message = msgRequired) ])
  vision          = TextAreaField("Vision",  validators = [ DataRequired(message = msgRequired) ])
  abbrevation     = StringField("Abbrevation",  validators = [ DataRequired(message = msgRequired) ])
  foundation_date = DateTimeLocalField('Founded Date', format='%Y-%m-%dT%H:%M')
  type            = SelectField("Type", choices = typeChoices, validators = [unselectedValid])

