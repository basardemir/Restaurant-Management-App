from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, RadioField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length
from wtforms_components import IntegerField
import psycopg2 as dbapi2
msg = "The column must be filled."

url="postgres://ivpallnyfezioy:075baf8e129b0d52dbd6d87dd3c774363b0b10b499921f821378ed7084bfc744@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dagmb1jla3rmdp"
connection = dbapi2.connect(url)
cursor = connection.cursor()
cursor.execute("select * from timezone")
timezone = cursor.fetchall()
cursor.close()

class CountryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message = msg),Length(max=30, min=4,message="Name length has to be between 4 and 30")])
    short_code = StringField("Short_Code", validators=[DataRequired(message=msg), Length(max=2, message="Country Code cannot be longer than 2 characters")])
    lane = RadioField("Driving Lane",choices=[("right","Right"), ("left", "Left")], default="right")
    Capital_City = StringField("Capital City", validators=[Length(max=30, message="Capital City name cannot be longer than 30 characters")])
    Language_Long = StringField("Language(long)", validators=[Length(max=15, message="Language Long cannot be longer than 15 characters")])
    Language_Short= StringField("Language(short)", validators=[Length(max=15, message="Language Short cannot be longer than 3 characters")])
    
    Area = FloatField("Area", validators=[NumberRange(min=0)])
    GDP = FloatField("GDP", validators=[NumberRange(min=0)])
    GDP_multiplier = SelectField("exp1",choices=[("1000","K"),("1000000","Mill"),("1000000000","Bill")])
    Population = IntegerField("Population", validators=[NumberRange(min=0)])
    Population_multiplier = SelectField("exp2",choices=[("1000","K"),("1000000","Mill"),("1000000000","Bill")])
    
    Longitude = FloatField("Longitude",validators=[NumberRange(min=-180, max=+180, message="Longitude needs to be between -180 and 180.")])
    Latitude = FloatField("Latitude", validators=[NumberRange(min=-90,max=90,message="Latitude needs to be between -90 and 90.")])
    timezone = SelectField("Timezone", choices=[(str(tz_id),tz_name) for tz_id, tz_name in timezone])