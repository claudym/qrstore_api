from flask_restful import Resource
from flask_jwt_extended import jwt_required
from http import HTTPStatus
from models.size import Size
from schemas.size import SizeSchema


size_schema = SizeSchema()
size_list_schema = SizeSchema(many=True)


class SizeListResource(Resource):
    @jwt_required()
    def get(self):
        size = Size.get_all()
        return size_list_schema.dump(size)


class SizeResource(Resource):
    @jwt_required()
    def get(self, size_id):
        size = Size.get_by_id(size_id)
        if size is None:
            return {"message": "Size not found"}, HTTPStatus.NOT_FOUND
        return size_schema.dump(size)
