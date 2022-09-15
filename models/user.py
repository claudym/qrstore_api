from extensions import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False, default=False)
    password = db.Column(db.String(120))
    first_name = db.Column(db.String(70))
    last_name = db.Column(db.String(70))
    tax_id = db.Column(db.String(50))
    photo = db.Column(db.String(100), default=None)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
