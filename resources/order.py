from decimal import Decimal
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from marshmallow import ValidationError
from sqlalchemy.exc import DatabaseError
from models.order import Order
from models.order_item import OrderItem
from models.product import Product
from models.product_snapshot import ProductSnapshot
from models.inventory import Inventory
from schemas.order import OrderSchema


order_schema = OrderSchema()
order_list_schema = OrderSchema(many=True)


class OrderListResource(Resource):
    @jwt_required()
    def get(self):
        orders = Order.get_all()
        return order_list_schema.dump(orders)

    @jwt_required()
    def post(self):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        try:
            data = order_schema.load(data=json_data)
        except ValidationError as err:
            return {
                "message": "Validation errors",
                "errors": err.messages,
            }, HTTPStatus.BAD_REQUEST
        data["user_id"] = current_user
        # Compute total and get product_snapshot_id_list
        order_items = data["order_items"]
        total = Decimal("0")
        product_snapshot_id_list = []
        for item in order_items:
            product = Product.get_by_id(item["product_id"])
            if product is None:
                return {
                    "message": f"Product with id ({item['product_id']} not found"
                }, HTTPStatus.NOT_FOUND
            # Get latest product_snapshot id from product_id
            product_snapshot = ProductSnapshot.get_by_product_latest(item["product_id"])
            total += product_snapshot.price * item["count"]
            product_snapshot_id_list.append(product_snapshot.id)
        data["total"] = total
        # Compare total with payment and set order_status_id
        if data["payment"] == data["total"]:
            data["order_status_id"] = 2  # 1-pending, 2-complete, 3-canceled
        else:
            data["order_status_id"] = 1  # 1-pending, 2-complete, 3-canceled
        # Save order
        # ==========
        del data["order_items"]
        order = Order(**data)
        try:
            order.save()
        except DatabaseError as err:
            return {
                "message": "Database errors",
                "errors": str(err.orig),
            }, HTTPStatus.BAD_REQUEST
        order_dump = order_schema.dump(order)
        # Save order items(inside for loop)
        # ================
        for i in range(len(order_items)):
            order_item_data = {
                "order_id": order_dump["id"],
                "product_snapshot_id": product_snapshot_id_list[i],
                "count": order_items[i]["count"],
            }
            order_item = OrderItem(**order_item_data)
            try:
                order_item.save()
            except DatabaseError as err:
                # delete order record (atomic)
                # delete all order_item records so far (atomic)
                return {
                    "message": "Database errors",
                    "errors": str(err.orig),
                }, HTTPStatus.BAD_REQUEST
            # Update inventory per item
            # =========================
            inventory = Inventory.get_by_product_id(order_items[i]["product_id"])
            if inventory is None:
                return {"message": "Product not in inventory"}, HTTPStatus.BAD_REQUEST
            delta = inventory.count - order_items[i]["count"]
            if delta < 0:
                return {
                    "message": f"Count cannot be less than 0. (product_id: {order_items[i]['product_id']}, inventory_count: {inventory.count})"
                }
            inventory.count -= order_items[i]["count"]
            try:
                inventory.save()
            except DatabaseError as err:
                # delete order record (atomic)
                # delete all order_item records so far (atomic)
                return {
                    "message": "Database errors",
                    "errors": str(err.orig),
                }, HTTPStatus.BAD_REQUEST

        print("inventory.count", inventory.count)  # testing
        return order_dump, HTTPStatus.CREATED
