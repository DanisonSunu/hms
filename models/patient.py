from models.database import db

class Patient(db.Model):
    __tablename__ = 'patients'
    patient_id        = db.Column(db.Integer, primary_key=True)
    name              = db.Column(db.String(100), nullable=False)
    age               = db.Column(db.Integer,     nullable=False)
    gender            = db.Column(db.String(10),  nullable=False)
    phone             = db.Column(db.String(15),  nullable=False)
    address           = db.Column(db.Text)
    blood_group       = db.Column(db.String(5))
    registration_date = db.Column(db.DateTime, server_default=db.func.now())
    appointments = db.relationship('Appointment',   backref='patient', lazy=True, cascade='all, delete-orphan')
    records      = db.relationship('MedicalRecord', backref='patient', lazy=True, cascade='all, delete-orphan')
    bills        = db.relationship('Billing',       backref='patient', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {'patient_id':self.patient_id,'name':self.name,'age':self.age,
                'gender':self.gender,'phone':self.phone,'address':self.address,
                'blood_group':self.blood_group,'registration_date':str(self.registration_date)}
