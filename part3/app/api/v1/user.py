from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask import request
from app.services import facade
from werkzeug.security import generate_password_hash

api = Namespace('users', description='User operations')

# ====== MODELS ======
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user')
})

login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# ====== PUBLIC ROUTES ======

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return new_user.to_dict(), 201

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'You cannot modify email or password')
    @api.response(403, 'Unauthorized')
    def put(self, user_id):
        """Update user info (cannot modify email or password)"""
        current_user = get_jwt_identity()
        if current_user['id'] != user_id:
            return {'error': 'Unauthorized'}, 403

        if 'email' in api.payload or 'password' in api.payload:
            return {'error': 'You cannot modify email or password'}, 400

        try:
            updated_user = facade.update_user(user_id, api.payload)
            return updated_user.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/login')
class UserLogin(Resource):
    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return JWT"""
        data = api.payload
        user = facade.get_user_by_email(data['email'])

        if not user or not user.check_password(data['password']):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(identity={
            'id': user.id,
            'email': user.email,
            'is_admin': user.is_admin
        })
        return {'access_token': access_token}, 200

# ====== ADMIN ROUTES ======

@api.route('/admin/users/')
class AdminUserListCreate(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Admin: Create a user"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        email = user_data.get('email')

        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return new_user.to_dict(), 201

    @jwt_required()
    @api.response(200, 'User list retrieved successfully')
    @api.response(403, 'Admin privileges required')
    def get(self):
        """Admin: Get all users"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        all_users = facade.get_all_users()
        return [user.to_dict() for user in all_users], 200

@api.route('/admin/users/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Email already in use')
    @api.response(403, 'Admin privileges required')
    def put(self, user_id):
        """Admin: Update a user"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = api.payload
        email = data.get('email')

        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        if 'password' in data:
            data['password'] = generate_password_hash(data['password'])

        updated_user = facade.update_user(user_id, data)
        return updated_user.to_dict(), 200

    @jwt_required()
    @api.response(204, 'User deleted successfully')
    @api.response(404, 'User not found')
    @api.response(403, 'Admin privileges required')
    def delete(self, user_id):
        """Admin: Delete a user"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        facade.delete_user(user_id)
        return '', 204