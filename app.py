import logging
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_uploads import configure_uploads
from flask_cors import CORS
from extensions import db, jwt, image_set
from resources.token import (
    TokenResource,
    RefreshTokenResource,
    RevokeTokenResource,
    block_list,
)
from resources.user import (
    UserListResource,
    UserResource,
    MeResource,
    UserPhotoUploadResource,
)
from resources.product import (
    ProductListResource,
    ProductResource,
    ProductImageUploadResource,
)
from resources.product_snapshot import ProductSnapshotResource
from resources.inventory import InventoryListResource, InventoryResource
from resources.sex import SexListResource, SexResource
from resources.size import SizeListResource, SizeResource
from resources.order import OrderListResource, OrderResource
from resources.order_status import OrderStatusListResource, OrderStatusResource
from resources.payment_method import PaymentMethodListResource, PaymentMethodResource
from resources.role import RoleListResource, RoleResource
from models.order_item import OrderItem  # pylint: disable=unused-import


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config.DevelopmentConfig")
    register_extensions(app)
    register_resources(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)  # pylint: disable=unused-variable
    jwt.init_app(app)
    configure_uploads(app, image_set)
    CORS(app)

    @jwt.token_in_blocklist_loader
    # pylint: disable-next=unused-argument
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
    api.add_resource(UserPhotoUploadResource, "/user/photo")
    api.add_resource(MeResource, "/me")
    api.add_resource(RoleListResource, "/role")
    api.add_resource(RoleResource, "/role/<int:role_id>")
    api.add_resource(ProductListResource, "/product")
    api.add_resource(ProductResource, "/product/<int:product_id>")
    api.add_resource(ProductImageUploadResource, "/product/<int:product_id>/image")
    api.add_resource(
        ProductSnapshotResource, "/product-snapshot/<int:product_snapshot_id>"
    )
    api.add_resource(InventoryListResource, "/inventory")
    api.add_resource(InventoryResource, "/inventory/<int:product_id>")
    api.add_resource(SexListResource, "/sex")
    api.add_resource(SexResource, "/sex/<int:sex_id>")
    api.add_resource(SizeListResource, "/size")
    api.add_resource(SizeResource, "/size/<int:size_id>")
    api.add_resource(OrderListResource, "/order")
    api.add_resource(OrderResource, "/order/<int:order_id>")
    api.add_resource(OrderStatusListResource, "/order-status")
    api.add_resource(OrderStatusResource, "/order-status/<int:order_status_id>")
    api.add_resource(PaymentMethodListResource, "/payment-method")
    api.add_resource(PaymentMethodResource, "/payment-method/<int:payment_method_id>")


server = create_app()
gunicorn_error_logger = logging.getLogger("gunicorn.error")
server.logger.handlers.extend(gunicorn_error_logger.handlers)
server.logger.setLevel(logging.DEBUG)
