from decimal import Decimal
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from marshmallow import ValidationError
from sqlalchemy.exc import DatabaseError
from models.user import User
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
        total = Decimal("0.00")
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
        if data["payment"] > total:
            return {
                "message": f"Payment cannot be more than total (${total:,})"
            }, HTTPStatus.BAD_REQUEST
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
        # order_dump["order_items"] = order_items
        # Save order items(inside for loop)
        # ================
        for i in range(len(order_items)):
            order_item_data = {
                "order_id": order_dump["id"],
                "product_snapshot_id": product_snapshot_id_list[i],
                "count": order_items[i]["count"],
            }
            order_item = OrderItem(**order_item_data)
            del order_item_data["order_id"]
            order_dump["order_items"].append(order_item_data)
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
                }, HTTPStatus.BAD_REQUEST
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
        return order_dump, HTTPStatus.CREATED


class OrderResource(Resource):
    @jwt_required()
    def get(self, order_id):
        order = Order.get_by_id(order_id)
        if order is None:
            return {"message": "Order not found"}, HTTPStatus.NOT_FOUND
        return order_schema.dump(order)

    @jwt_required()
    def patch(self, order_id):
        json_data = request.get_json()
        try:
            data = order_schema.load(
                data=json_data,
                partial=(
                    "payment",
                    "payment_method_id",
                    "customer_name",
                    "customer_phone",
                    "customer_email",
                    "tax_id",
                    "order_status_id",
                ),
            )
        except ValidationError as err:
            return {
                "message": "Validation errors",
                "errors": err.messages,
            }, HTTPStatus.BAD_REQUEST

        order = Order.get_by_id(order_id)
        if order is None:
            return {"message": "Order not found"}, HTTPStatus.NOT_FOUND
        if order.order_status_id == 3:  # canceled
            return {"message": "This order has been canceled"}, HTTPStatus.BAD_REQUEST
        current_user = get_jwt_identity()
        if (
            data.get("order_status_id") == 3
            and User.get_by_id(current_user).role_id > 2
        ):  # status: canceled and role: user
            return {
                "message": "This user is not authorized to cancel orders"
            }, HTTPStatus.FORBIDDEN
        order.user_id = current_user
        if data.get("order_status_id") == 3:
            for item in order.order_items:
                product_snapshot = ProductSnapshot.get_by_id(item.product_snapshot_id)
                inventory = Inventory.get_by_product_id(product_snapshot.product_id)
                inventory.count += item.count
                try:
                    inventory.save()
                except DatabaseError as err:
                    return {
                        "message": "Database errors",
                        "errors": str(err.orig),
                    }, HTTPStatus.BAD_REQUEST
            order.order_status_id = 3
            try:
                order.save()
            except DatabaseError as err:
                return {
                    "message": "Database errors",
                    "errors": str(err.orig),
                }, HTTPStatus.BAD_REQUEST
            return order_schema.dump(order)
        if order.order_status_id == 2:
            return {
                "message": "You cannot change content of a complete order"
            }, HTTPStatus.BAD_REQUEST
        if data.get("payment") is not None:
            if data.get("payment") <= order.payment:
                return {
                    "message": "Payment has to be greater than last payment"
                }, HTTPStatus.BAD_REQUEST
            if data.get("payment") > order.total:
                return {
                    "message": "Payment has to be less than or equal to total"
                }, HTTPStatus.BAD_REQUEST
            order.payment = data.get("payment")
            if order.payment == order.total:
                order.order_status_id = 2
        order.payment_method_id = (
            data.get("payment_method_id") or order.payment_method_id
        )
        order.customer_name = data.get("customer_name") or order.customer_name
        order.customer_phone = data.get("customer_phone") or order.customer_phone
        order.customer_email = data.get("customer_email") or order.customer_email
        order.tax_id = data.get("tax_id") or order.tax_id

        try:
            order.save()
        except DatabaseError as err:
            return {
                "message": "Database errors",
                "errors": str(err.orig),
            }, HTTPStatus.BAD_REQUEST
        return order_schema.dump(order)
