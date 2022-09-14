from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.product import Product


class ProductListResource(Resource):
    def get(self):
        products = Product.get_all()
        print(products) # test

        return {'data': products}
    
    # def post(self):

class ProductResource(Resource):
    def get(self, product_id):
        product = Product.get_by_id(product_id)
        print(product) # test
        return {'data': product}, HTTPStatus.OK
