from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField , IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):

    Cname = StringField('Consultant Name',
                           validators=[DataRequired()])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class sentimentform(FlaskForm):
    q1=StringField('Q1- What you have been thinking from past few days? ',validators=[DataRequired(),Length(min=15,max=40)])
    q2=StringField('Q2- How is your social life?',validators=[DataRequired(),Length(min=15,max=40)])
    q3=StringField('Q3- Describe your work place.',validators=[DataRequired(),Length(min=15,max=40)])
    q4=StringField('Q4- Comment on your family.',validators=[DataRequired(),Length(min=15,max=40)])
    q5=StringField('Q5- How often do you procrastinate about the status of your personal goals in life?',validators=[DataRequired(),Length(min=15,max=40)])
    submit=SubmitField('Result')
    result=IntegerField('your result is')
