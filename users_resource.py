import datetime
from flask import jsonify, request
from flask_restful import abort, Resource
from db import db_session
from data.User import User
from users_parser import parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f'User #{user_id} not found.')


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({
            'user': user.to_dict(only=(
                'id',
                'name',
                'surname',
                'age',
                'position',
                'speciality',
                'address',
                'email',
                'modified_date',
                'city_from'
            ))
        })

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify(
            {
                'users': [item.to_dict(only=(
                    'id',
                    'name',
                    'surname',
                    'age',
                    'position',
                    'speciality',
                    'address',
                    'email',
                    'modified_date',
                    'city_from'
                )) for item in users]
            }
        )

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            city_from=args['city_from']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
