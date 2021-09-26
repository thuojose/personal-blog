from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import Required

class BlogForm(FlaskForm):
    title = StringField('Blog title', validators = [Required()])
    content = TextAreaField('Blog content', validators = [Required()])
    submit = SubmitField('Submit')
