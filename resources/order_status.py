from flask_restful import Resource
from flask_jwt_extended import jwt_required
from http import HTTPStatus
from models.order_status import OrderStatus
from schemas.order_status import OrderStatusSchema

order_status_schema = OrderStatusSchema()
order_status_list_schema = OrderStatusSchema(many=True)


class OrderStatusListResource(Resource):
    @jwt_required()
    def get(self):
        order_status = OrderStatus.get_all()
        return order_status_list_schema.dump(order_status)


class OrderStatusResource(Resource):
    @jwt_required()
    def get(self, order_status_id):
        order_status = OrderStatus.get_by_id(order_status_id)
        if order_status is None:
            return {"message": "OrderStatus not found"}, HTTPStatus.NOT_FOUND
        return order_status_schema.dump(order_status)
