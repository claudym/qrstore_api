from flask_restful import Resource
from flask_jwt_extended import jwt_required
from http import HTTPStatus
from models.sex import Sex
from schemas.sex import SexSchema


sex_schema = SexSchema()
sex_list_schema = SexSchema(many=True)


class SexListResource(Resource):
    @jwt_required()
    def get(self):
        sex = Sex.get_all()
        return sex_list_schema.dump(sex)


class SexResource(Resource):
    @jwt_required()
    def get(self, sex_id):
        sex = Sex.get_by_id(sex_id)
        if sex is None:
            return {"message": "Sex not found"}, HTTPStatus.NOT_FOUND
        return sex_schema.dump(sex)
