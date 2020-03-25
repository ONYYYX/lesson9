import flask
from db import db_session
from data.Jobs import Jobs

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_news():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return flask.jsonify(
        {
            'jobs': [item.to_dict(only=(
                'id', 'leader_id', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'
            )) for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>',  methods=['GET'])
def get_one_news(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if job:
        return flask.jsonify(
            {
                'jobs': job.to_dict(only=(
                    'id', 'leader_id', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'
                ))
            }
        )
    return flask.jsonify({'error': 'Not Found'})
