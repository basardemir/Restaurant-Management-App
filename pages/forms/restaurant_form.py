from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, RadioField, FloatField, IntegerField, FileField, SubmitField, FormField, DateField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError
from wtforms.fields.html5 import DateField
from wtforms_components import IntegerField
# from ..forms.company_form import Company
# from ..forms.users_form import ContactInfoForm
import psycopg2 as dbapi2

msg = "This field is required to be filled!"

url="postgres://ivpallnyfezioy:075baf8e129b0d52dbd6d87dd3c774363b0b10b499921f821378ed7084bfc744@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dagmb1jla3rmdp"
def contact_info_extractor():
    connection = dbapi2.connect(url)
    cursor = connection.cursor()
    statement = "select id, phonenumber, email from contactinfo;"
    cursor.execute(statement)
    contact_info = cursor.fetchall()
    contact_dict = {}
    contact_dict[0] = "Select Contact info..."
    for item in reversed(contact_info):
        contact_dict[item[0]] = "Phone Number:"+str(item[1])+", Email:"+str(item[2])
    return contact_dict

def company_extractor():
    connection = dbapi2.connect(url)
    cursor = connection.cursor()
    statement = "select company_id, name, information from company;"
    cursor.execute(statement)
    companies = cursor.fetchall()
    company_dict = {}
    company_dict[0] = "Select company..."
    for item in reversed(companies):
        company_dict[item[0]] = "Name:"+str(item[1])+", Info:"+str(item[2])
    return company_dict
    


class Restaurant_Form(FlaskForm):
    score = FloatField("Score", validators=[DataRequired(message=msg), Length(min=1, max=5, message="Score must be between 1-5")], render_kw={'placeholder': "Score",  "class" : "form-control"})
    capacity = FloatField("Capacity", validators=[DataRequired(message=msg)], render_kw={'placeholder': "Capacity of the restaurant",  "class" : "form-control"})
    
    opening_date = DateField("Opening Date", render_kw={"class" : "form-control"})
    
    manager = StringField("Manager", validators=[DataRequired(message=msg)], render_kw={'placeholder': "Manager",  "class" : "form-control"})
    total_earning = FloatField("total_earning", validators=[DataRequired(message=msg)], render_kw={'placeholder': "Total Earnings",  "class" : "form-control"})

class ContactInfoForm(FlaskForm):
    contact = SelectField("Contact Info", validators=[DataRequired(message=msg)], choices=[(str(key), value) for key, value in contact_info_extractor().items()], default=0)

class Company(FlaskForm):
    company = SelectField("Company", validators=[DataRequired(message=msg)], choices=[item for item in company_extractor().items()], default=0)

class Restaurant_Page(FlaskForm):
    restaurant = FormField(Restaurant_Form)
    company = FormField(Company)
    contact_info = FormField(ContactInfoForm)
    submit_button = SubmitField( render_kw = { "class" : "btn btn-primary"})



