from flask_restful import Resource
from flask_jwt_extended import jwt_required
from http import HTTPStatus
from models.role import Role
from schemas.role import RoleSchema


role_schema = RoleSchema()
role_list_schema = RoleSchema(many=True)


class RoleListResource(Resource):
    @jwt_required()
    def get(self):
        role = Role.get_all()
        return role_list_schema.dump(role)


class RoleResource(Resource):
    @jwt_required()
    def get(self, role_id):
        role = Role.get_by_id(role_id)
        if role is None:
            return {"message": "Role not found"}, HTTPStatus.NOT_FOUND
        return role_schema.dump(role)
