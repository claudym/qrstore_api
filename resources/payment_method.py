from flask_restful import Resource
from flask_jwt_extended import jwt_required
from http import HTTPStatus
from models.payment_method import PaymentMethod
from schemas.payment_method import PaymentMethodSchema


payment_method_schema = PaymentMethodSchema()
payment_method_list_schema = PaymentMethodSchema(many=True)


class PaymentMethodListResource(Resource):
    @jwt_required()
    def get(self):
        payment_method = PaymentMethod.get_all()
        return payment_method_list_schema.dump(payment_method)


class PaymentMethodResource(Resource):
    @jwt_required()
    def get(self, payment_method_id):
        payment_method = PaymentMethod.get_by_id(payment_method_id)
        if payment_method is None:
            return {"message": "PaymentMethod not found"}, HTTPStatus.NOT_FOUND
        return payment_method_schema.dump(payment_method)
