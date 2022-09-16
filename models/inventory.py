from extensions import db


class Inventory(db.Model):
    __tablename__ = "inventory"
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=False,
        unique=True,
        primary_key=True,
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(),
        nullable=False,
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_product_id(cls, product_id):
        return cls.query.filter_by(product_id=product_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
