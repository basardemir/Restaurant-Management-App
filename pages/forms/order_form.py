from flask import request, session
from flask_wtf import FlaskForm
from wtforms import Field, RadioField, DecimalField, SubmitField, FormField, StringField, TextAreaField, SelectField, ValidationError, FieldList
from wtforms.validators import DataRequired, Length
#from wtforms.fields.html5 import DateField
from wtforms.fields.html5 import DateTimeLocalField

from datetime import datetime, timedelta
from ..forms.users_form import UserAccountForm, ContactInfoForm, PersonForm

from models.users import select_users

msgRequired = "The {} must be filled."
msgChosen   = "Must choose one {} of them."

class Order(FlaskForm):
  note = TextAreaField(
    "Note", 
    validators = [ DataRequired(message = msgRequired.format("note") )],
    render_kw = { "class" : "form-control" }
  )
  
  price = DecimalField(
    "Price",
    render_kw = {"class": "form-control", "readonly" : True}
  )

  payment_type = SelectField(
    "Payment Type",
    choices = [("CASH", "Cash"), ("CREDIT", "Credit Card")],
    validators = [ DataRequired(message = msgRequired.format("payment type")) ],
    render_kw = { "class" : "form-control"}
  )

  end_at = DateTimeLocalField(
    'End Datetime',
    format = '%Y-%m-%dT%H:%M',
    default = ( datetime.now() + timedelta(minutes=(60)) ),
    render_kw = { "class" : "form-control" }
  )

  rate = RadioField(
    "Rate",
    default = 0,
    coerce=int,
    choices = [ (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), ],
    validators = [ DataRequired(message = msgRequired.format("rate"))],
    render_kw = { "class" : "list-group list-group-horizontal" }
  )

class OrderForm(FlaskForm):
  order     = FormField(Order)
  submit    = SubmitField( render_kw = { "class" : "btn btn-primary"})
