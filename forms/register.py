from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    city_from = StringField('Город на Земле', validators=[DataRequired()])
    submit = SubmitField('Войти')
