from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id =db.Column(db.String(50))
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)

    @classmethod
    def find_by_username(cls, user):
      return cls.query.filter_by(name = user).first()
