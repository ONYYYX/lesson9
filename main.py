from flask import Flask
from db import db_session
from data.User import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_skey_lol_lmao'
db_session.global_init('db/blogs.sqlite')


def main():
    # для запуска приложения, меняйте почту, она должна быть уникальной
    user = User()
    user.surname = 'iuawdvnawjd'
    user.name = 'awdvawidmwkamdnkv'
    user.age = 3
    user.position = 'child'
    user.speciality = 'child'
    user.address = 'module_123'
    user.email = 'scott_is_father_ahahah@mars.org'
    user.hashed_password = '1234124'
    session = db_session.create_session()
    session.add(user)
    session.commit()

    app.run()


if __name__ == '__main__':
    main()
