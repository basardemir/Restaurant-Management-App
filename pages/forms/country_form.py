from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, RadioField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length
from wtforms_components import IntegerField

msg = "The column must be filled."

class CountryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message = msg),Length(max=30, message="Name cannot be longer than 30 characters")])
    short_code = StringField("Short_Code", validators=[DataRequired(message=msg), Length(max=2, message="Country Code cannot be longer than 2 characters")])
    lane = RadioField("Driving_Lane",choices=[("right","Right"), ("left", "Left")], default="right")
    Capital_City = StringField("Capital_City", validators=[Length(max=30, message="Capital City name cannot be longer than 30 characters")])
    Language_Long = StringField("LLong", validators=[Length(max=15, message="Language Long cannot be longer than 15 characters")])
    Language_Short= StringField("SLong", validators=[Length(max=15, message="Language Short cannot be longer than 3 characters")])
    
    Area = IntegerField("Area", validators=[NumberRange(min=0)])
    GDP = IntegerField("GDP", validators=[NumberRange(min=0)])
    GDP_multiplier = SelectField("exp1",choices=[("K",1000),("M",1000000),("B",1000000000)])
    Population = IntegerField("Population", validators=[NumberRange(min=0)])
    Population_multiplier = SelectField("exp2",choices=[("K",1000),("M",1000000),("B",1000000000)])
    
    Longitude = FloatField("lon",validators=[NumberRange(min=-180, max=+180, message="Longitude needs to be between -180 and 180.")])
    Latitude = FloatField("lat", validators=[NumberRange(min=-90,max=90,message="Latitude needs to be between -90 and 90.")])
