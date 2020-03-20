from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    job = StringField('Почта', validators=[DataRequired()])
    leader_id = IntegerField('ID Лидера', validators=[DataRequired()])
    work_size = IntegerField('Часы на выполнение', validators=[DataRequired()])
    collaborators = StringField('Сотрудники')
    is_finished = BooleanField('Закончена?')
    submit = SubmitField('Добавить')
