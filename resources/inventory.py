from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy.exc import DatabaseError
from http import HTTPStatus
from models.inventory import Inventory
from models.user import User
from schemas.inventory import InventorySchema


inventory_schema = InventorySchema()
inventory_list_schema = InventorySchema(many=True)


class InventoryListResource(Resource):
    @jwt_required()
    def get(self):
        inventory = Inventory.get_all()
        return inventory_list_schema.dump(inventory)

    @jwt_required()
    def post(self):
        json_data = request.get_json()
        try:
            data = inventory_schema.load(data=json_data)
        except ValidationError as err:
            return {
                "message": "Validation errors",
                "errors": err.messages,
            }, HTTPStatus.BAD_REQUEST

        current_user = get_jwt_identity()
        if User.get_by_id(current_user).role_id > 2:  # 1-Admin, 2-Manager, 3-User
            return {"message": "Access is not allowed"}, HTTPStatus.FORBIDDEN

        data["user_id"] = current_user
        inventory = Inventory(**data)
        try:
            inventory.save()
        except DatabaseError as err:
            return {
                "message": "Database errors",
                "errors": str(err.orig),
            }, HTTPStatus.BAD_REQUEST
        return inventory_schema.dump(inventory)
