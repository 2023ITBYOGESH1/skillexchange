from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, FileField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        Length(max=120, message='Email must be less than 120 characters')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])


class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        Length(max=120, message='Email must be less than 120 characters')
    ])
    bio = TextAreaField('Bio', validators=[
        Optional(),
        Length(max=500, message='Bio must be less than 500 characters')
    ])
    location = StringField('Location', validators=[
        Optional(),
        Length(max=120, message='Location must be less than 120 characters')
    ])
    profile_picture = FileField('Profile Picture', validators=[Optional()])
    signature = FileField('Signature (for certificates)', validators=[Optional()])


class SkillForm(FlaskForm):
    title = StringField('Skill Title', validators=[
        DataRequired(message='Skill title is required'),
        Length(min=2, max=100, message='Title must be between 2 and 100 characters')
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(message='Description is required'),
        Length(min=10, max=1000, message='Description must be between 10 and 1000 characters')
    ])
    category = SelectField('Category', choices=[
        ('', 'Select a category'),
        ('technology', 'Technology & Programming'),
        ('language', 'Languages'),
        ('music', 'Music & Audio'),
        ('art', 'Art & Design'),
        ('business', 'Business & Finance'),
        ('health', 'Health & Fitness'),
        ('cooking', 'Cooking & Baking'),
        ('crafts', 'Crafts & DIY'),
        ('sports', 'Sports & Games'),
        ('academic', 'Academic & Education'),
        ('other', 'Other')
    ], validators=[DataRequired(message='Please select a category')])
    skill_type = SelectField('Skill Type', choices=[
        ('offered', 'I can teach this'),
        ('wanted', 'I want to learn this')
    ], validators=[DataRequired(message='Please select skill type')])


class ExchangeRequestForm(FlaskForm):
    message = TextAreaField('Message', validators=[
        Optional(),
        Length(max=500, message='Message must be less than 500 characters')
    ])


class MessageForm(FlaskForm):
    content = StringField('Message', validators=[
        DataRequired(message='Message cannot be empty'),
        Length(max=1000, message='Message must be less than 1000 characters')
    ])


class ReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[
        DataRequired(message='Rating is required'),
        NumberRange(min=1, max=5, message='Rating must be between 1 and 5')
    ])
    comment = TextAreaField('Comment', validators=[
        Optional(),
        Length(max=500, message='Comment must be less than 500 characters')
    ])


class ReportForm(FlaskForm):
    reason = TextAreaField('Reason', validators=[
        DataRequired(message='Please provide a reason for reporting'),
        Length(min=10, max=500, message='Reason must be between 10 and 500 characters')
    ])


class AdminUserEditForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        Length(max=120, message='Email must be less than 120 characters')
    ])
    bio = TextAreaField('Bio', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])
    is_admin = SelectField('Admin Status', choices=[
        ('0', 'Normal User'),
        ('1', 'Admin')
    ])
    is_banned = SelectField('Ban Status', choices=[
        ('0', 'Not Banned'),
        ('1', 'Banned')
    ])


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])


class SearchForm(FlaskForm):
    query = StringField('Search', validators=[Optional()])
    category = SelectField('Category', choices=[
        ('', 'All Categories'),
        ('technology', 'Technology & Programming'),
        ('language', 'Languages'),
        ('music', 'Music & Audio'),
        ('art', 'Art & Design'),
        ('business', 'Business & Finance'),
        ('health', 'Health & Fitness'),
        ('cooking', 'Cooking & Baking'),
        ('crafts', 'Crafts & DIY'),
        ('sports', 'Sports & Games'),
        ('academic', 'Academic & Education'),
        ('other', 'Other')
    ], validators=[Optional()])
    skill_type = SelectField('Type', choices=[
        ('', 'All Types'),
        ('offered', 'Offering'),
        ('wanted', 'Wanted')
    ], validators=[Optional()])

