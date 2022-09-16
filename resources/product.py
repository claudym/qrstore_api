from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from marshmallow import ValidationError
from sqlalchemy.exc import DatabaseError
from models.user import User
from models.product import Product
from models.product_snapshot import ProductSnapshot
from schemas.product import ProductSchema


product_schema = ProductSchema()
product_list_schema = ProductSchema(many=True)


class ProductListResource(Resource):
    @jwt_required()
    def get(self):
        products = Product.get_all()
        return product_list_schema.dump(products)

    @jwt_required()
    def post(self):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        try:
            data = product_schema.load(data=json_data)
        except ValidationError as err:
            return {
                "message": "Validation errors",
                "errors": err.messages,
            }, HTTPStatus.BAD_REQUEST

        product = Product(**data)
        product.user_id = current_user
        product_db = Product.get_by_desc_price_size(
            product.desc, product.price, product.size
        )
        if product_db is not None:
            return {
                "message": "Product with same description, price, size, and sex exists"
            }, HTTPStatus.BAD_REQUEST

        try:
            product.save()
        except DatabaseError as err:
            return {
                "message": "Database errors",
                "errors": str(err.orig),
            }, HTTPStatus.BAD_REQUEST

        data = product_schema.dump(product)
        data["product_id"] = data["id"]
        data["user_id"] = current_user
        del data["id"]
        del data["created_at"]
        del data["updated_at"]

        product_snapshot = ProductSnapshot(**data)
        try:
            product_snapshot.save()
        except DatabaseError as err:
            product.rollback()
            return {
                "message": "Database errors",
                "errors": str(err.orig),
            }, HTTPStatus.BAD_REQUEST
        return product_schema.dump(product), HTTPStatus.CREATED


class ProductResource(Resource):
    @jwt_required()
    def get(self, product_id):
        product = Product.get_by_id(product_id)
        if product is None:
            return {"message": "Product not found"}, HTTPStatus.NOT_FOUND
        return product_schema.dump(product)

    @jwt_required()
    def delete(self, product_id):
        product = Product.get_by_id(product_id)
        if product is None:
            return {"message": "Product not found"}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if User.get_by_id(current_user).role_id > 2:  # 1-Admin, 2-Manager, 3-User
            return {"message": "Access is not allowed"}, HTTPStatus.FORBIDDEN

        product.delete()
        return {}, HTTPStatus.NO_CONTENT

    @jwt_required()
    def patch(self, product_id):
        json_data = request.get_json()
        try:
            data = product_schema.load(data=json_data, partial=("desc",))
        except ValidationError as err:
            return {
                "message": "Validation errors",
                "errors": err.messages,
            }, HTTPStatus.BAD_REQUEST

        product = Product.get_by_id(product_id)
        if product is None:
            return {"message": "Product not found"}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if User.get_by_id(current_user).role_id > 2:  # 1-Admin, 2-Manager, 3-User
            return {"message": "Access is not allowed"}, HTTPStatus.FORBIDDEN

        product.desc = data.get("desc") or product.desc
        product.price = data.get("price") or product.price
        product.size = data.get("size") or product.size
        product.user_id = current_user

        try:
            product.save()
        except DatabaseError as err:
            return {
                "message": "Database errors",
                "errors": str(err.orig),
            }, HTTPStatus.BAD_REQUEST

        data = product_schema.dump(product)
        data["product_id"] = data["id"]
        data["user_id"] = current_user
        del data["id"]
        del data["created_at"]
        del data["updated_at"]

        product_snapshot = ProductSnapshot(**data)
        try:
            product_snapshot.save()
        except DatabaseError as err:
            product.rollback()
            return {
                "message": "Database errors",
                "errors": str(err.orig),
            }, HTTPStatus.BAD_REQUEST
        return product_schema.dump(product)
