from extensions import db


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey("size.id"))
    sex_id = db.Column(db.Integer, db.ForeignKey("sex.id"))
    kid = db.Column(db.Boolean(), nullable=False)
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
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, product_id):
        return cls.query.filter_by(id=product_id).first()

    @classmethod
    def get_by_desc_price_size_sex(cls, desc, price, size_id, sex_id):
        return cls.query.filter_by(
            desc=desc, price=price, size_id=size_id, sex_id=sex_id
        ).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback()
