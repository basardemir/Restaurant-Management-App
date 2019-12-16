from flask_wtf import FlaskForm
from wtforms import SubmitField, FormField, StringField, TextAreaField, SelectField, ValidationError, FloatField
from wtforms.validators import DataRequired, NumberRange, Length
from wtforms_components import IntegerField

msgRequired = "The {} must be filled."
msgLength   = "The {} has to be between {} and {}"

class Comment(FlaskForm):
  title = StringField(
    "Title",
    validators = [ 
      DataRequired(message = msgRequired.format("Title")),
      Length(min=1, max=50, message = msgLength.format("Title", 1, 50))
    ],
    render_kw = { "class" : "form-control" }
  )
  
  description = TextAreaField(
    "Description", 
    validators = [ 
      DataRequired(message = msgRequired.format("Description")),
      Length(min=1, max=300, message = msgLength.format("Description", 1, 300))
    ],
    render_kw = { "class" : "form-control" }
  )

class CommentForm(FlaskForm):
  comment = FormField(Comment)
  submit  = SubmitField( render_kw = { "class" : "btn btn-primary"})
