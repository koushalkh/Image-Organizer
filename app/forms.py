from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired,FileAllowed
from werkzeug.utils import secure_filename


class LoginForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired()])
	password=PasswordField('Password',validators=[DataRequired()])
	remember_me=BooleanField('Remember Me')
	submit=SubmitField('Sign In')

class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])


class SignupForm(FlaskForm):
	username=StringField('username',validators=[DataRequired()])
	email=StringField('email',validators=[DataRequired()])
	password=StringField('password',validators=[DataRequired()])
	age=StringField('age',validators=[DataRequired()])
	mobile=StringField('mobile',validators=[DataRequired()])
	submit=SubmitField('Sign Up')


class UploadForm(FlaskForm):
	photo = FileField(validators=[FileRequired()])
	submit=SubmitField('Upload')
