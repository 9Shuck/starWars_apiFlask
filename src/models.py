from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel(db.Model):

    def create(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        get_all = cls.query.all()
        return get_all

    @classmethod
    def get_by_id(cls, id):
        user = cls.query.get(id)
        return user

    def disable_user(self):
        self.is_active = False
        db.session.commit()

    def get_all_favourites(cls, id):
        get_favourites = cls.query.filter_by(id=user_id)
        return get_favourites

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

