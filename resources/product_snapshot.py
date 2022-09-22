from flask_restful import Resource
from flask_jwt_extended import jwt_required
from http import HTTPStatus
from models.product_snapshot import ProductSnapshot
from schemas.product_snapshot import ProductSnapshotSchema


product_snapshot_schema = ProductSnapshotSchema()


class ProductSnapshotResource(Resource):
    @jwt_required()
    def get(self, product_snapshot_id):
        product_snapshot = ProductSnapshot.get_by_id(product_snapshot_id)
        if product_snapshot is None:
            return {"message": "Product snapshot not found"}, HTTPStatus.NOT_FOUND
        return product_snapshot_schema.dump(product_snapshot)
