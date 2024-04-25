from app import db, bcrypt, marshmallow
from datetime import datetime

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True, nullable=False)
    email = db.Column(db.String(255), unique=True, index=True,nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    def set_password(self, hash_key):
        self.password_hash = bcrypt.generate_password_hash(hash_key).decode('utf8')

    def check_password(self, hash_key):
        return bcrypt.check_password_hash(self.password_hash, hash_key)

    def __repr__(self):
        return '<User %r>' % self.username

class UsersSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Users