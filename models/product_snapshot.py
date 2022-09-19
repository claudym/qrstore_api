from extensions import db


class ProductSnapshot(db.Model):
    __tablename__ = "product_snapshot"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey("size.id"))
    sex_id = db.Column(db.Integer, db.ForeignKey("sex.id"))
    kid = db.Column(db.Boolean(), nullable=False)
    user_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())

    @classmethod
    def get_by_id(cls, product_snapshot_id):
        return cls.query.filter_by(id=product_snapshot_id).first()

    @classmethod
    def get_by_product_latest(cls, product_id):
        return (
            cls.query.filter_by(product_id=product_id).order_by(cls.id.desc()).first()
        )

    def save(self):
        db.session.add(self)
        db.session.commit()
