from flask_wtf import FlaskForm
from wtforms import Field, SubmitField, FormField, StringField, TextAreaField, SelectField, ValidationError, FieldList
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField
#from wtforms.fields.html5 import DateTimeLocalField

from datetime import datetime

from ..forms.users_form import UserAccountForm, ContactInfoForm, PersonForm

msgRequired = "The {} must be filled."
msgChosen   = "Must choose one {} of them."

typeChoices = [
  ('-1', 'Choose one!'), 
  ('LTD', 'Limited'), 
  ('AS', 'Anonim')
]

def unselectedValid(form, field):
  if field.data == "-1":
    raise ValidationError(msgChosen.format(field.name))    

class Company(FlaskForm):
  
  name = StringField(
    "Name", 
    validators = [ DataRequired(message = msgRequired.format("name") )],
    render_kw = { "class" : "form-control" }
  )

  information = TextAreaField(
    "Information", 
    validators = [ DataRequired(message = msgRequired.format("Information")) ],
    render_kw = { "class" : "form-control" }
  )

  mission = TextAreaField(
    "Mission",
    validators = [ DataRequired(message = msgRequired.format("Mission")) ],
    render_kw = { "class" : "form-control" }
  )

  vision = TextAreaField(
    "Vision",
    validators = [ DataRequired(message = msgRequired.format("Vision")) ],
    render_kw = { "class" : "form-control" }
  )

  abbrevation = StringField(
    "Abbrevation",
    validators = [ DataRequired(message = msgRequired.format("Abbrevation")) ],
    render_kw = { "class" : "form-control" }
  )

  foundation_date = DateField(
    'Founded Date', 
    render_kw = { "class" : "form-control" }
  )

  type = SelectField(
    "Type", 
    choices = typeChoices, 
    validators = [ unselectedValid ],
    render_kw = { "class" : "form-control" }
  )


class CompanyForm(FlaskForm):
  company   = FormField(Company)
  contact   = FormField(ContactInfoForm)
  submit    = SubmitField( render_kw = { "class" : "btn btn-primary"})
