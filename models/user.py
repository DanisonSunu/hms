from flask_login import UserMixin
from models.database import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id    = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(80),  nullable=False, unique=True)
    password   = db.Column(db.String(256), nullable=False)
    role       = db.Column(db.String(20),  nullable=False)
    linked_id  = db.Column(db.Integer,     nullable=True)
    created_at = db.Column(db.DateTime,    server_default=db.func.now())

    def get_id(self): return str(self.user_id)

    @property
    def is_admin(self):  return self.role == 'admin'
    @property
    def is_doctor(self): return self.role == 'doctor'
    @property
    def is_staff(self):  return self.role == 'staff'
