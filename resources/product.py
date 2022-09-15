from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from marshmallow import ValidationError
from sqlalchemy.exc import DatabaseError
from models.product import Product
from schemas.product import ProductSchema


product_schema = ProductSchema()
product_list_schema = ProductSchema(many=True)


class ProductListResource(Resource):
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
            return {'message': 'Validation errors', 'errors': err.messages}, HTTPStatus.BAD_REQUEST

        product = Product(**data)
        product.user_id = current_user
        
        try:
            product.save()
        except DatabaseError as err:
            return {'message': 'Database errors', 'errors': str(err.orig)}, HTTPStatus.BAD_REQUEST
        return product_schema.dump(product), HTTPStatus.CREATED

class ProductResource(Resource):
    def get(self, product_id):
        product = Product.get_by_id(product_id)
        return {'data': product}, HTTPStatus.OK
