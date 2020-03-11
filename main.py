from flask import Flask, render_template
from db import db_session
from data.Jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_skey_lol_lmao'
db_session.global_init('db/blogs.sqlite')


@app.route('/')
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs)
    return render_template('jobs.html', jobs=jobs)


def main():
    app.run()


if __name__ == '__main__':
    main()
