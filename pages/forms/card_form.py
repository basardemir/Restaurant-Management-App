from flask_wtf import FlaskForm
from wtforms import SelectField, FormField, SubmitField, StringField, RadioField, ValidationError
from wtforms.validators import DataRequired, Optional, Length
from wtforms_components import IntegerField, ColorField
from wtforms.fields.html5 import DateField
from colour import Color
from datetime import datetime, timedelta

from flask import session

from models.card import check_card_number
from models.users import check_if_user_exists, select_a_user_and_info, get_user_by_username


msgRequired = "The {} must be filled."
msgChosen   = "Must choose one {} of them."
msgValidations = [
  "Username not found.",
  "This user is not a customer!"
]
typeChoices = [
  (0, 'Inactive'), 
  (1, 'Active')
]


def checkUser(form, field):
  
  if not check_if_user_exists( {"username":field.data} ):
    raise ValidationError(msgValidations[0])
  else:
    
    user_id = get_user_by_username(field.data)['id']
    
    t = select_a_user_and_info( user_id )[0]['membershiptype']
    if t != 'Customer':
      raise ValidationError(msgValidations[1])
  
class Card(FlaskForm):
  points = IntegerField(
    "Points",
    default = 0,
    validators = [ DataRequired(message = msgRequired.format("points"))],
    render_kw = { "class" : "form-control" }
  )
  
  is_active = RadioField(
    "Is Active",
    default = 1,
    choices = typeChoices, 
    coerce  = int,
    validators = [ DataRequired(message = msgRequired.format("active state") ) ],
    render_kw = { "class" : "list-group list-group-horizontal" }
  )

  color = ColorField(
    "Color", 
    validators = [ Optional() ],
    render_kw = { "class" : "form-control"}
  )

  expire_date = DateField(
    'Expire Date',
    default = ( datetime.now() + timedelta(days=(365)) ),
    render_kw = { "class" : "form-control" }
  )

  card_number = StringField(
    "Card Number",
    validators= [ Length(min=16, max=16, message = "The column size must be 16" )],
    render_kw = {"class": "form-control", "readonly" : True}
  )

class CardForm(FlaskForm):
  card      = FormField(Card)
  username  = StringField(
    "Username",
    validators = [ checkUser ],
    render_kw = { "class" : "form-control" }
  )
  submit    = SubmitField( render_kw = { "class" : "btn btn-primary"})


'''
companies = SelectField(
    "Companies", 
    choices = get_id_and_name_of_companies(), 
    validators = [ DataRequired() ],
    render_kw = { "class" : "form-control" }
  )
'''