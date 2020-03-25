from flask import jsonify, request, Blueprint
from db import db_session
from data.Jobs import Jobs

blueprint = Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'jobs': [item.to_dict(only=(
                'id', 'leader_id', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'
            )) for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>',  methods=['GET'])
def get_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if job:
        return jsonify(
            {
                'jobs': job.to_dict(only=(
                    'id', 'leader_id', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'
                ))
            }
        )
    return jsonify({'error': 'Not Found'})


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'leader_id', 'job', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    if session.query(Jobs).get(request.json['id']):
        return jsonify({'error': 'Id already exists'})
    job = Jobs(
        id=request.json['id'],
        leader_id=request.json['leader_id'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    session.add(job)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    session.delete(job)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_job(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Bad request'})
    if 'leader_id' in request.json:
        job.leader_id = request.json['leader_id']
    if 'job' in request.json:
        job.job = request.json['job']
    if 'work_size' in request.json:
        job.work_size = request.json['work_size']
    if 'collaborators' in request.json:
        job.collaborators = request.json['collaborators']
    if 'is_finished' in request.json:
        job.is_finished = request.json['is_finished']
    session.commit()
    return jsonify({'success': 'OK'})
