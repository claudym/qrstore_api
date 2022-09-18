from extensions import db


class Sex(db.Model):
    __tablename__ = "sex"
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(10), nullable=False, unique=True)

    @classmethod
    def get_by_id(cls, role_id):
        return cls.query.filter_by(id=role_id)
