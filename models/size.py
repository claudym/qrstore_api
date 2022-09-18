from extensions import db


class Size(db.Model):
    __tablename__ = "size"
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(10), nullable=False, unique=True)

    @classmethod
    def get_by_id(cls, size_id):
        return cls.query.filter_by(id=size_id).first()
