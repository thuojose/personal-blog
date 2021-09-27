from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Email,EqualTo
from wtforms import ValidationError
from ..models import User

class RegistrationForm(FlaskForm):
    email = StringField('',validators=[Required(),Email()], render_kw={"placeholder": "Enter your email address"})
    username = StringField('',validators = [Required()], render_kw={"placeholder": "Enter your preferred username"})
    password = PasswordField('',validators = [Required(), EqualTo('password_confirm',message = 'Passwords must match')], render_kw={"placeholder": "Preferred password"})
    password_confirm = PasswordField('',validators = [Required()], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField('Sign Up')
    
    # Custom validation
    def validate_email(self,data_field):
        if User.query.filter_by(email =data_field.data).first():
            raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is taken')
    
    
class LoginForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()], render_kw={"placeholder"})
    password = PasswordField('Password',validators =[Required()], render_kw={"placeholder": "Your password"})
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')