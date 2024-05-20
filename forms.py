from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class VegetableForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    expiration_date = DateField('Expiration Date', validators=[DataRequired()])
    supplier = StringField('Supplier', validators=[DataRequired()])
    submit = SubmitField('Submit')
