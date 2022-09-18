from extensions import db


class Sex(db.Model):
    __tablename__ = "sex"
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(10), nullable=False, unique=True)

    @classmethod
    def get_by_id(cls, sex_id):
        return cls.query.filter_by(id=sex_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()
