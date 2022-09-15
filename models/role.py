from extensions import db


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(30), nullable=False, unique=True)

    @classmethod
    def get_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()
