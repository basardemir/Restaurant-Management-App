from flask_wtf import FlaskForm
from wtforms import  FileField, SubmitField, FormField, PasswordField, StringField, TextAreaField, SelectField, RadioField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length, Regexp
from wtforms.fields.html5 import DateField

msg = "The field must be filled."


class PersonForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message = msg),Length(max=25, message="Username cannot be longer than 25 characters")], render_kw={"class": "form-control"})
    surname = StringField("Surname", validators=[DataRequired(message=msg), Length(max=25, message="Surname cannot be longer than 25 characters")], render_kw={"class": "form-control"})
    birthday = DateField("Birthday", validators=[DataRequired(message=msg)], render_kw={"class": "form-control"})
    educationLevel = RadioField("Education Level", choices=[("University","University"), ("High School", "High School"), ("Middle School", "Middle School"), ("Primary School", "Primary School")], default="University", render_kw={"class": "list-group list-group-horizontal"})
    gender = RadioField("Gender", choices=[("Female", "Female"), ("Male", "Male"), ("Other", "Other")], default="Female", render_kw={"class": "list-group list-group-horizontal"})

class UserAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message = msg),Length(max=25, message="Username cannot be longer than 25 characters")], render_kw={"class": "form-control"})
    password = PasswordField("Password", validators=[DataRequired(message=msg), Length(max=25, message="Password cannot be longer than 25 characters")], render_kw={"class": "form-control"})
    membershiptype = RadioField("Membership Type",choices=[("Boss","Boss"), ("Employee", "Employee")], default="Boss", render_kw={"class": "list-group list-group-horizontal"})
    securityAnswer = StringField("Security Answer", validators=[Length(max=30, message="Security answer cannot be longer than 30 characters")], render_kw={"class": "form-control", "placeholder": "What is your mother's maiden name?"})

class ContactInfoForm(FlaskForm):
    phoneNumber = StringField("Phone Number", validators=[DataRequired(message = msg),Length(max=20, message="Phone number cannot be longer than 25 characters")], render_kw={"class": "form-control"})
    email = StringField("Email", validators=[DataRequired(message = msg),Length(max=30, message="Email cannot be longer than 30 characters")], render_kw={"class": "form-control"})
    fax = StringField("Fax", validators=[DataRequired(message = msg),Length(max=30, message="Fax cannot be longer than 30 characters")], render_kw={"class": "form-control"})
    homePhone = StringField("Phone Number(Home)", validators=[DataRequired(message = msg),Length(max=50, message="Home phone number cannot be longer than 50 characters")], render_kw={"class": "form-control"})
    workmail = StringField("Work Email", validators=[DataRequired(message = msg),Length(max=50, message="Work email cannot be longer than 50 characters")], render_kw={"class": "form-control"})

class SocialMedia(FlaskForm):
    facebook = StringField("Facebook", validators=[DataRequired(message = msg),Length(max=60, message="Facebook cannot be longer than 60 characters")], render_kw={"class": "form-control"})
    twitter = StringField("Twitter", validators=[DataRequired(message = msg),Length(max=60, message="Twitter cannot be longer than 60 characters")], render_kw={"class": "form-control"})
    instagram = StringField("Instagram", validators=[DataRequired(message = msg),Length(max=60, message="Instagram cannot be longer than 60 characters")], render_kw={"class": "form-control"})
    discord = StringField("Discord", validators=[DataRequired(message = msg),Length(max=60, message="Discord cannot be longer than 60 characters")], render_kw={"class": "form-control"})
    youtube = StringField("Youtube", validators=[DataRequired(message = msg),Length(max=60, message="Youtube cannot be longer than 60 characters")], render_kw={"class": "form-control"})
    googleplus = StringField("Google+", validators=[DataRequired(message = msg),Length(max=60, message="Google+ cannot be longer than 60 characters")], render_kw={"class": "form-control"})

class PhotoForm(FlaskForm):
    photo = FileField("Photo", validators=[DataRequired(message = msg)])

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
