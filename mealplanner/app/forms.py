from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class addMeal(FlaskForm):
    date = StringField("Date")
    title = StringField("Title")
    url = StringField("URL")
    ingredients = TextAreaField("Ingredients", render_kw={"rows": 8, "cols": 60})
    notes = TextAreaField("Notes", render_kw={"rows": 2, "cols": 60})
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
