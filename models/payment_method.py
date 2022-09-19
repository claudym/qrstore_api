from extensions import db


class PaymentMethod(db.Model):
    __tablename__ = "payment_method"
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(20), nullable=False, unique=True)

    @classmethod
    def get_by_id(cls, payment_method_id):
        return cls.query.filter_by(id=payment_method_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()
