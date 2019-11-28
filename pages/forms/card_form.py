from flask_wtf import FlaskForm
from wtforms import FormField, SubmitField, StringField, RadioField, ValidationError
from wtforms.validators import DataRequired, Optional
from wtforms_components import IntegerField, ColorField
from wtforms.fields.html5 import DateField
from colour import Color
from datetime import datetime, timedelta

msgRequired = "The {} must be filled."
msgChosen   = "Must choose one {} of them."

typeChoices = [
  (0, 'Inactive'), 
  (1, 'Active')
]

class Card(FlaskForm):
  points = IntegerField(
    "Points",
    validators = [ DataRequired(message = msgRequired.format("points") )],
    render_kw = { "class" : "form-control" }
  )

  card_number = StringField(
    "Card Number", 
    validators = [ DataRequired(message = msgRequired.format("card number") )],
    render_kw = { "class" : "form-control" }
  )
  
  is_active = RadioField(
    "Is Active", 
    choices = typeChoices, 
    coerce=int,
    validators = [ DataRequired(message = msgRequired.format("active state") ) ],
    render_kw = { "class" : "form-control list-group" }
  )

  color = ColorField(
    "Color", 
    validators = [ Optional() ],
    render_kw = { "class" : "form-control"}
  )

  activation_date = DateField(
    'Activation Date',
    default = datetime.today,
    render_kw = { "class" : "form-control" }
  )
  expire_date = DateField(
    'Expire Date',
    default = ( datetime.now() + timedelta(days=(365*2)) ),
    render_kw = { "class" : "form-control" }
  )

class CardForm(FlaskForm):
  card = FormField(Card)
  submit  = SubmitField( render_kw = { "class" : "btn btn-primary"})
