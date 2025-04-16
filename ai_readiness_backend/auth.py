from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from models import User, db
from flask_bcrypt import generate_password_hash
import bcrypt

auth_ns = Namespace('auth', description='User Authentication')

# Input models
register_model = auth_ns.model('Register', {
    'full_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})

login_model = auth_ns.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    def post(self):
        data = request.get_json()
        email = data['email'].lower()

        if User.query.filter_by(email=email).first():
            return {'message': 'User already exists.'}, 409

        user = User(
            full_name=data['full_name'],
            email=email,
        )
        user.password = data['password']  # This will hash the password

        db.session.add(user)
        db.session.commit()

        return {'message': 'User registered successfully.'}, 201


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        email = data['email'].lower()
        password = data['password']

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return {'message': 'Invalid email or password.'}, 401

        access_token = create_access_token(identity=user.id)
        return {
            'message': 'Login successful.',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role
            }
        }
