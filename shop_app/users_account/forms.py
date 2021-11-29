from wtforms import StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError
from flask_wtf.file import FileAllowed, file_required, file_allowed, FileField
from wtforms import form
from wtforms.form import Form
from flask_wtf import FlaskForm
from .models import Register


class UserRegisterationForm(FlaskForm):
    fname = StringField('First Name: ', [validators.DataRequired()])
    lname = StringField('Last Name: ', [validators.DataRequired()])
    email = StringField(
        'Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired(
    ), validators.EqualTo('confirm', message='Both Password must match')])
    confirm = PasswordField('Confirm Password: ', [validators.DataRequired()])
    country = StringField('Country: ', [validators.DataRequired()])
    state = StringField('State: ', [validators.DataRequired()])
    city = StringField('City: ', [validators.DataRequired()])
    zipcode = StringField('Zip Code: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()])
    contact = StringField('Contact: ', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileAllowed(
        ['jpeg,jpg,png,gif'], 'Upload Images only')])

    submit = SubmitField('Register')

    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError('This email address is already taken')




class UserLoginForm(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])