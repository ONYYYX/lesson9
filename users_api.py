from datetime import datetime
from flask import jsonify, request, Blueprint
from db import db_session
from data.User import User

blueprint = Blueprint('users_api', __name__, template_folder='templates')


@blueprint.route('/api/users')
def get_users():
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


@blueprint.route('/api/users/<int:user_id>',  methods=['GET'])
def get_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if user:
        return jsonify(
            {
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
            }
        )
    return jsonify({'error': 'Not Found'})


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'name', 'surname', 'age', 'position', 'speciality', 'address', 'email']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    if session.query(User).get(request.json['id']):
        return jsonify({'error': 'Id already exists'})
    user = User(
        id=request.json['id'],
        name=request.json['name'],
        surname=request.json['surname'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email']
    )
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Bad request'})
    if 'name' in request.json:
        user.name = request.json['name']
    if 'surname' in request.json:
        user.surname = request.json['surname']
    if 'age' in request.json:
        user.age = request.json['age']
    if 'position' in request.json:
        user.position = request.json['position']
    if 'speciality' in request.json:
        user.speciality = request.json['speciality']
    if 'address' in request.json:
        user.address = request.json['address']
    if 'email' in request.json:
        user.email = request.json['email']
    user.modified_date = datetime.now()
    session.commit()
    return jsonify({'success': 'OK'})
