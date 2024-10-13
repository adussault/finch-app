from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, SelectMultipleField

from wtforms.validators import AnyOf, DataRequired
from .app_data import providers, products

class CreateSandbox(FlaskForm):
	name = StringField('Session Name', 
		validators=[DataRequired()])
	provider = SelectField(
		'Provider', 
		choices=list(providers.keys()),
		validators=[DataRequired()])
	products = SelectMultipleField(
		'Products',
		choices=products, 
		validators=[DataRequired()])
	submit = SubmitField('Submit')


