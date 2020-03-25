from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired, Email


class DepartmentForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    chief_id = IntegerField('ID Лидера', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    members = StringField('Сотрудники')
    submit = SubmitField('Добавить')
