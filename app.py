from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from config import Config
from extensions import db, jwt
from resources.token import (
    TokenResource,
    RefreshTokenResource,
    RevokeTokenResource,
    block_list,
)
from resources.user import UserListResource, UserResource, MeResource
from resources.product import ProductListResource, ProductResource
from models.role import Role


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config.DevelopmentConfig")
    register_extensions(app)
    register_resources(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in block_list


def register_resources(app):
    api = Api(app)
    api.add_resource(TokenResource, "/token")
    api.add_resource(RefreshTokenResource, "/refresh")
    api.add_resource(RevokeTokenResource, "/revoke")
    api.add_resource(UserListResource, "/users")
    api.add_resource(UserResource, "/user/<string:username>")
    api.add_resource(MeResource, "/me")
    api.add_resource(ProductListResource, "/products")
    api.add_resource(ProductResource, "/product/<int:product_id>")


if __name__ == "__main__":
    app = create_app()
    app.run()
