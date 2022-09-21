from extensions import db


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    total = db.Column(db.Numeric(), nullable=False)
    order_status_id = db.Column(db.Integer, db.ForeignKey("order_status.id"))
    payment_method_id = db.Column(db.Integer, db.ForeignKey("payment_method.id"))
    payment = db.Column(db.Numeric(), nullable=False)
    customer_name = db.Column(db.String(100))
    customer_phone = db.Column(db.String(20))
    customer_email = db.Column(db.String(100))
    tax_id = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(),
        nullable=False,
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )
    order_items = db.relationship('OrderItem', backref='order_item')

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, order_id):
        return cls.query.filter_by(id=order_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
