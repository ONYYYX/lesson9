from flask import jsonify, request
from flask_restful import abort, Resource
from db import db_session
from data.Jobs import Jobs
from jobs_parser import parser


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f'Job #{job_id} not found.')


class JobResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({
            'job': job.to_dict(only=(
                'id',
                'leader_id',
                'job',
                'work_size',
                'collaborators',
                'start_date',
                'end_date',
                'is_finished'
            ))
        })

    def put(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        if not request.json:
            return jsonify({'error': 'Empty request'})
        user = session.query(Jobs).get(job_id)
        if 'leader_id' in request.json:
            user.leader_id = request.json['leader_id']
        if 'job' in request.json:
            user.job = request.json['job']
        if 'work_size' in request.json:
            user.work_size = request.json['work_size']
        if 'collaborators' in request.json:
            user.collaborators = request.json['collaborators']
        if 'is_finished' in request.json:
            user.is_finished = request.json['is_finished']
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify(
            {
                'jobs': [item.to_dict(only=(
                    'id',
                    'leader_id',
                    'job',
                    'work_size',
                    'collaborators',
                    'start_date',
                    'end_date',
                    'is_finished'
                )) for item in jobs]
            }
        )

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            leader_id=args['leader_id'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})
