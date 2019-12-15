from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, RadioField, FloatField, IntegerField, FileField, SubmitField, FormField, DateField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError
from wtforms.fields.html5 import DateField
from wtforms_components import IntegerField
import psycopg2 as dbapi2

msg = "This field is required to be filled!"
url="postgres://ivpallnyfezioy:075baf8e129b0d52dbd6d87dd3c774363b0b10b499921f821378ed7084bfc744@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dagmb1jla3rmdp"
def restaurant_extractor():
    connection = dbapi2.connect(url)
    cursor = connection.cursor()
    statement = "select restaurant_id, company.name, manager from (restaurant join company on company_belongs = company_id);"
    cursor.execute(statement)
    rests = cursor.fetchall()
    rest_dict = {}
    rest_dict[0] = "Select restaurant.."
    for item in reversed(rests):
        rest_dict[item[0]] = "Name: "+str(item[1])+", Manager: "+str(item[2])
    return rest_dict

class Ingredient_Form(FlaskForm):
    ingred_name = StringField("Name", validators=[DataRequired(message=msg), Length(min=3, max=50, message="Name lenght must be between 4-30!")], render_kw={'placeholder': "Ingredient Name (eg. Potato)",  "class" : "form-control"})
    ingred_type = StringField("Type", validators=[DataRequired(message=msg), ], render_kw={"placeholder":"Ingredient Type (eg. Vegetable)",  "class" : "form-control"})
    unit_weight = FloatField("Unit Weight", validators=[DataRequired(message=msg), NumberRange(min=0)], render_kw={'placeholder': "Unit Weight (g)",  "class" : "form-control"})
    volume = FloatField("Volume", validators=[DataRequired(message=msg), NumberRange(min=0)], render_kw={'placeholder': "Volume",  "class" : "form-control"})
    ideal_temp = FloatField("Ideal Temperature", validators=[NumberRange(min=-10, max=50), DataRequired(message=msg)], render_kw={'placeholder': "Ideal Temperature (in Celcius)",  "class" : "form-control"})

class Photo_Form(FlaskForm):
    photo = FileField("Photo", validators=[DataRequired(message = msg)], render_kw={"accept": ".jpg"})

class Nutrition_Form(FlaskForm):
    protein =  FloatField("Protein", validators=[DataRequired(message=msg), NumberRange(min=0)], render_kw={'placeholder': "Protein (per 100g)",  "class" : "form-control"})
    fat = FloatField("Fat", validators=[DataRequired(message=msg), NumberRange(min=0)], render_kw={'placeholder': "Fat (per 100g)",  "class" : "form-control"})
    carbohydrates = FloatField("Carbohydrates", validators=[DataRequired(message=msg), NumberRange(min=0)], render_kw={'placeholder': "Carbohydrates (per 100g)",  "class" : "form-control"})
    cholesterol = FloatField("Cholesterol", validators=[DataRequired(message=msg), NumberRange(min=0)], render_kw={'placeholder': "Cholesterol (per 100g)",  "class" : "form-control"})
    calories = FloatField("Calories", validators=[DataRequired(message=msg), NumberRange(min=0)], render_kw={'placeholder': "Calories (per 100g)",  "class" : "form-control"})
    
class Restaurant(FlaskForm):
    restaurant = SelectField("Restaurant", validators=[DataRequired(message=msg)], choices=[item for item in restaurant_extractor().items()])
    stock = FloatField("Stock Amount", validators=[DataRequired(message=msg), NumberRange(min=0)], render_kw={'placeholder': "Stock Amount",  "class" : "form-control"})
    expire_date = DateField("Expire Date", render_kw={"class" : "form-control"})    

class Ingredient_Page(FlaskForm):
    ingredient = FormField(Ingredient_Form)
    nutrition = FormField(Nutrition_Form)
    photo = FormField(Photo_Form)
    restaurant = FormField(Restaurant)
    submit_button = SubmitField( render_kw = { "class" : "btn btn-primary"})

class Ing_with_Button(FlaskForm):
    ingredient = FormField(Ingredient_Form)
    submit_button = SubmitField( render_kw = { "class" : "btn btn-primary"})