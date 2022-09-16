from extensions import db


class ProductSnapshot(db.Model):
    __tablename__ = 'product_snapshot'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    desc = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(), nullable=False)
    size = db.Column(db.String(50))
    image = db.Column(db.String(100), default=None)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(),
        nullable=False,
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )

    @classmethod
    def get_by_id(cls, product_snapshot_id):
        return cls.query.filter_by(id=product_snapshot_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
