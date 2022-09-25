import os
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from marshmallow import ValidationError
from sqlalchemy.exc import DatabaseError
from extensions import image_set
from utils import save_image
from models.user import User
from schemas.user import UserSchema


user_schema = UserSchema()
user_photo_schema = UserSchema(only=("photo_url",))
user_public_schema = UserSchema(
    exclude=("email", "first_name", "last_name", "tax_id", "created_at", "updated_at")
)


class UserListResource(Resource):
    @jwt_required(optional=True)  # remove optional for production
    def post(self):
        json_data = request.get_json()
        try:
            data = user_schema.load(data=json_data)
        except ValidationError as err:
            return {
                "message": "Validation errors",
                "errors": err.messages,
            }, HTTPStatus.BAD_REQUEST
        if User.get_by_username(data.get("username")):
            return {"message": "username already used."}, HTTPStatus.BAD_REQUEST
        if User.get_by_email(data.get("email")):
            return {"message": "email already used."}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        try:
            user.save()
        except DatabaseError as err:
            return {
                "message": "Validation errors",
                "errors": str(err.orig),
            }, HTTPStatus.BAD_REQUEST
        return user_schema.dump(user), HTTPStatus.CREATED


class UserResource(Resource):
    @jwt_required()
    def get(self, username):
        user = User.get_by_username(username)
        if user is None:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user == user.id or User.get_by_id(current_user).role_id < 3:
            return user_schema.dump(user)
        return user_public_schema.dump(user)


class MeResource(Resource):
    @jwt_required()
    def get(self):
        user = User.get_by_id(get_jwt_identity())
        return user_schema.dump(user)


class UserPhotoUploadResource(Resource):
    @jwt_required()
    def put(self):
        file = request.files.get("photo")
        if not file:
            return {"message": "Not a valid image"}, HTTPStatus.BAD_REQUEST
        if not image_set.file_allowed(file, file.filename):
            return {"message": "File type not allowed"}, HTTPStatus.BAD_REQUEST
        user = User.get_by_id(get_jwt_identity())
        if user.photo:
            photo_path = image_set.path(folder="photos", filename=user.photo)
            if os.path.exists(photo_path):
                os.remove(photo_path)
        filename = save_image(image=file, folder="photos")
        user.photo = filename
        user.save()
        return user_photo_schema.dump(user), HTTPStatus.OK
