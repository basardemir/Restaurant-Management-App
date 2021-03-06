from flask_wtf import FlaskForm
from wtforms import SelectField, FileField, SubmitField, FormField, PasswordField, StringField, TextAreaField, SelectField, RadioField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length, Regexp, Email
from wtforms.fields.html5 import DateField
from models.location_model import get_all_location_with_dict

msg = "The field must be filled."


class PersonForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message = msg),Length(max=25, message="Username cannot be longer than 25 characters")], render_kw={"class": "form-control"})
    surname = StringField("Surname", validators=[DataRequired(message=msg), Length(max=25, message="Surname cannot be longer than 25 characters")], render_kw={"class": "form-control"})
    birthday = DateField("Birthday", validators=[DataRequired(message=msg)], render_kw={"class": "form-control"})
    educationLevel = RadioField("Education Level", choices=[("University","University"), ("High School", "High School"), ("Middle School", "Middle School"), ("Primary School", "Primary School")], default="University", render_kw={"class": "list-group list-group-horizontal"})
    gender = SelectField("Gender", choices=[("Female", "Female"), ("Male", "Male"), ("Other", "Other")], default="Female", render_kw={"class": "custom-select"})

class UserAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message = msg),Length(max=25, message="Username cannot be longer than 25 characters")], render_kw={"class": "form-control"})
    password = PasswordField("Password", validators=[DataRequired(message=msg), Length(max=25, message="Password cannot be longer than 25 characters")], render_kw={"class": "form-control"})
    membershiptype = RadioField("Membership Type",choices=[("Boss","Boss"), ("Customer", "Customer")], default="Boss", render_kw={"class": "list-group list-group-horizontal"})
    securityAnswer = TextAreaField("Security Answer", validators=[Length(max=30, message="Security answer cannot be longer than 30 characters")], render_kw={"class": "form-control", "placeholder": "What is your mother's maiden name?"})

class ContactInfoForm(FlaskForm):
    phoneNumber = StringField("Phone Number", validators=[Regexp(regex="^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$", message="Not a valid phone number"), DataRequired(message = msg),Length(max=20, message="Phone number cannot be longer than 25 characters")], render_kw={"class": "form-control"})
    email = StringField("Email", validators=[Email(message="Not a valid email"), DataRequired(message = msg),Length(max=30, message="Email cannot be longer than 30 characters")], render_kw={"class": "form-control"})
    fax = StringField("Fax", validators=[Regexp(regex="^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$", message="Not a valid fax number"), DataRequired(message = msg),Length(max=30, message="Fax cannot be longer than 30 characters")], render_kw={"class": "form-control"})
    homePhone = StringField("Phone Number(Home)", validators=[DataRequired(message = msg),Length(max=50, message="Home phone number cannot be longer than 50 characters")], render_kw={"class": "form-control"})
    workmail = StringField("Work Email", validators=[Email(message="Not a valid work email"), DataRequired(message = msg),Length(max=50, message="Work email cannot be longer than 50 characters")], render_kw={"class": "form-control"})
    locations = get_all_location_with_dict()
    options = []
    for item in locations:
        options.append((item['location_id'], item["street"] + ", " + item["neighborhood"] + "," + item["county"] + "," + item["province_name"] + "," + item["name"] + "," + item["zipcode"]))
    location = SelectField("Location", coerce=int, choices=options,  render_kw={"class": "custom-select"})

class SocialMedia(FlaskForm):
    facebook = StringField("Facebook", validators=[Regexp(regex="(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", message="Not a valid Facebook link"),DataRequired(message = msg),Length(max=60, message="Facebook cannot be longer than 60 characters")], render_kw={"class": "form-control"})
    twitter = StringField("Twitter", validators=[Regexp(regex="(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", message="Not a valid Twitter link"), DataRequired(message = msg),Length(max=60, message="Twitter cannot be longer than 60 characters")], render_kw={"class": "form-control"})
    instagram = StringField("Instagram", validators=[Regexp(regex="(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", message="Not a valid Instagram link"), DataRequired(message = msg),Length(max=60, message="Instagram cannot be longer than 60 characters")], render_kw={"class": "form-control"})
    discord = StringField("Discord", validators=[Regexp(regex="(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", message="Not a valid Discord link"), DataRequired(message = msg),Length(max=60, message="Discord cannot be longer than 60 characters")], render_kw={"class": "form-control"})
    youtube = StringField("Youtube", validators=[Regexp(regex="(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", message="Not a valid Youtube link"), DataRequired(message = msg),Length(max=60, message="Youtube cannot be longer than 60 characters")], render_kw={"class": "form-control"})
    linkedin = StringField("LinkedIn", validators=[Regexp(regex="(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", message="Not a valid Google+ link"), DataRequired(message = msg),Length(max=60, message="Google+ cannot be longer than 60 characters")], render_kw={"class": "form-control"})

class PhotoForm(FlaskForm):
    photo = FileField("Photo", validators=[DataRequired(message = msg)], render_kw={"accept": ".jpg"})

class Combine(FlaskForm):
    person = FormField(PersonForm)
    useraccount = FormField(UserAccountForm)
    contactinfo = FormField(ContactInfoForm)
    socialmedia = FormField(SocialMedia)
    photo = FormField(PhotoForm)
    submit = SubmitField("Sign Up", render_kw={"class": "btn btn-outline-info"})


class CallSocialMedia(FlaskForm):
    socialmedia = FormField(SocialMedia)
    submit = SubmitField("Update", render_kw={"class": "btn btn-outline-info"})

class CallContactInfo(FlaskForm):
    contactinfo = FormField(ContactInfoForm)
    submit = SubmitField("Update", render_kw={"class": "btn btn-outline-info"})

class CallPerson(FlaskForm):
    person = FormField(PersonForm)
    submit = SubmitField("Update", render_kw={"class": "btn btn-outline-info"})

class UserEditAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message = msg),Length(max=25, message="Username cannot be longer than 25 characters")], render_kw={"class": "form-control"})
    password = PasswordField("Password", validators=[DataRequired(message=msg), Length(max=25, message="Password cannot be longer than 25 characters")], render_kw={"class": "form-control"})
    securityAnswer = StringField("Security Answer", validators=[Length(max=30, message="Security answer cannot be longer than 30 characters")], render_kw={"class": "form-control", "placeholder": "What is your mother's maiden name?"})

class CallUserAccount(FlaskForm):
    user = FormField(UserEditAccountForm)
    submit = SubmitField("Update", render_kw={"class": "btn btn-outline-info"})
