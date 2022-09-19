from extensions import db


class OrderStatus(db.Model):
    __tablename__ = "order_status"
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(15), nullable=False, unique=True)

    @classmethod
    def get_by_id(cls, order_status_id):
        return cls.query.filter_by(id=order_status_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()
