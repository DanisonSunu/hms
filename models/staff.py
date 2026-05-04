from models.database import db

class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id   = db.Column(db.Integer,     primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    role       = db.Column(db.String(50),  nullable=False)
    phone      = db.Column(db.String(15),  nullable=False)
    email      = db.Column(db.String(120), unique=True)
    department = db.Column(db.String(100))
    join_date  = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {'staff_id':self.staff_id,'name':self.name,'role':self.role,
                'phone':self.phone,'email':self.email,'department':self.department}
