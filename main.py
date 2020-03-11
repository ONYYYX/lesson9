from flask import Flask
from db import db_session
from data.Jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_skey_lol_lmao'
db_session.global_init('db/blogs.sqlite')


def main():
    job = Jobs()
    job.leader_id = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.is_finished = False
    session = db_session.create_session()
    session.add(job)
    session.commit()

    app.run()


if __name__ == '__main__':
    main()
