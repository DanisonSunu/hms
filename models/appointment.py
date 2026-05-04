from models.database import db

class Appointment(db.Model):
    __tablename__ = 'appointments'
    appointment_id = db.Column(db.Integer, primary_key=True)
    patient_id     = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    doctor_id      = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'),   nullable=False)
    date           = db.Column(db.String(20), nullable=False)
    time           = db.Column(db.String(10), nullable=False)
    status         = db.Column(db.String(20), default='Scheduled')
    notes          = db.Column(db.Text)
    created_at     = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {'appointment_id':self.appointment_id,'patient_id':self.patient_id,
                'patient_name':self.patient.name if self.patient else '',
                'doctor_id':self.doctor_id,'doctor_name':self.doctor.name if self.doctor else '',
                'date':self.date,'time':self.time,'status':self.status,'notes':self.notes}
