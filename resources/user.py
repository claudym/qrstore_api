from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from utils import hash_password
from models.user import User


class UserListResource(Resource):
    @jwt_required(optional=True)
    def post(self):
        json_data = request.get_json()
        username = json_data.get('username')
        email = json_data.get('email')
        if User.get_by_username(username):
            return {'message': 'username already used.'}, HTTPStatus.BAD_REQUEST
        if User.get_by_email(email):
            return {'message': 'email already used.'}, HTTPStatus.BAD_REQUEST
        
        non_hash_password = json_data.get('password')
        hashed = hash_password(non_hash_password)
        first_name = json_data.get('first_name')
        last_name = json_data.get('last_name')
        tax_id = json_data.get('tax_id')
        photo = json_data.get('photo')
        user = User(
            username=username,
            email=email,
            hashed=hashed,
            first_name=first_name,
            last_name=last_name,
            tax_id=tax_id,
            photo=photo
        )
        user.save()
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'tax_id': user.tax_id,
            'photo': user.photo
        }
        return data, HTTPStatus.CREATED


class UserResource(Resource):
    @jwt_required(optional=True)
    def get(self,  username):
        user = User.get_by_username(username)
        if user is None:
            return {'message': 'user not found.'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()
        if current_user == user.id:
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'tax_id': user.tax_id,
                'photo': user.photo
                # 'role_id': user.role_id
            }
        else:
            data = {
                'id': user.id,
                'username': user.username
            }
        return data, HTTPStatus.OK
