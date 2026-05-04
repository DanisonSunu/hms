from models.database import db

class Doctor(db.Model):
    __tablename__ = 'doctors'
    doctor_id      = db.Column(db.Integer,     primary_key=True)
    name           = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    phone          = db.Column(db.String(15),  nullable=False)
    email          = db.Column(db.String(120), unique=True)
    experience     = db.Column(db.Integer, default=0)
    available      = db.Column(db.Integer, default=1)
    appointments = db.relationship('Appointment',   backref='doctor', lazy=True)
    records      = db.relationship('MedicalRecord', backref='doctor', lazy=True)

    def to_dict(self):
        return {'doctor_id':self.doctor_id,'name':self.name,'specialization':self.specialization,
                'phone':self.phone,'email':self.email,'experience':self.experience,'available':bool(self.available)}
