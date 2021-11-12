from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, MultipleFileField, FloatField, IntegerField,SelectField
from wtforms.validators import InputRequired, Email


class UserSignupForm(FlaskForm):
    # email, password, submit_button
    first_name = StringField('First Name', validators = [InputRequired()])
    last_name = StringField('Last Name', validators = [InputRequired()])
    email = StringField('Email',validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    confirm = PasswordField('Repeat Password')
    submit_button = SubmitField()


class UserLoginForm(FlaskForm):
    # email, password, submit_button
    email = StringField('Email',validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    submit_button = SubmitField()


class ProductUploadForm(FlaskForm):
    title = StringField('Name', validators = [InputRequired()])
    description = StringField('Description', validators= [InputRequired()])
    tags = StringField('tags',description='separate tags with commas')
    category = SelectField('category')
    weight = FloatField('weight')
    price = IntegerField('price')
    creation_cost = IntegerField('cost of creation')
    stock = SelectField('Stock Number', choices = [i for i in range(1,11)])
    images = MultipleFileField('Images')
    submit_button = SubmitField()



class CategoryUploadForm(FlaskForm):
    category = StringField('Category Name')
    submit_button = SubmitField()