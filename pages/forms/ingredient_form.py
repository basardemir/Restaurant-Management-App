from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, RadioField, FloatField, IntegerField, FileField, SubmitField, FormField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError
from wtforms_components import IntegerField

msg = "This field is required to be filled!"

class Ingredient_Form(FlaskForm):
    ingred_name = StringField("Name", validators=[DataRequired(message=msg), Length(min=3, max=50, message="Name lenght must be between 4-30!")], render_kw={'placeholder': "Ingredient Name (eg. Potato)",  "class" : "form-control"})
    ingred_type = StringField("Type", validators=[DataRequired(message=msg), ], render_kw={"placeholder":"Ingredient Type (eg. Vegetable)",  "class" : "form-control"})
    unit_weight = FloatField("Unit Weight", validators=[DataRequired(message=msg), NumberRange(min=0)], render_kw={'placeholder': "Unit Weight (g)",  "class" : "form-control"})
    volume = FloatField("Volume", validators=[DataRequired(message=msg), NumberRange(min=0)], render_kw={'placeholder': "Volume",  "class" : "form-control"})
    ideal_temp = FloatField("Ideal_Temperature", validators=[NumberRange(min=-10, max=50), DataRequired(message=msg)], render_kw={'placeholder': "Ideal Temperature (in Celcius)",  "class" : "form-control"})

class Photo_Form(FlaskForm):
    photo = FileField("Photo", validators=[DataRequired(message = msg)], render_kw={"accept": ".jpg"})

class Nutrition_Form(FlaskForm):
    protein =  FloatField("Protein", validators=[DataRequired(message=msg), NumberRange(min=0)], render_kw={'placeholder': "Protein (per 100g)",  "class" : "form-control"})
    fat = FloatField("Fat", validators=[DataRequired(message=msg), NumberRange(min=0)], render_kw={'placeholder': "Fat (per 100g)",  "class" : "form-control"})
    carbohydrates = FloatField("Carbohydrates", validators=[DataRequired(message=msg), NumberRange(min=0)], render_kw={'placeholder': "Carbohydrates (per 100g)",  "class" : "form-control"})
    cholesterol = FloatField("Cholesterol", validators=[DataRequired(message=msg), NumberRange(min=0)], render_kw={'placeholder': "Cholesterol (per 100g)",  "class" : "form-control"})
    calories = FloatField("Calories", validators=[DataRequired(message=msg), NumberRange(min=0)], render_kw={'placeholder': "Calories (per 100g)",  "class" : "form-control"})
    
class Ingredient_Page(FlaskForm):
    ingredient = FormField(Ingredient_Form)
    nutrition = FormField(Nutrition_Form)
    photo = FormField(Photo_Form)
    submit_button = SubmitField( render_kw = { "class" : "btn btn-primary"})