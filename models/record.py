from models.database import db

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    record_id    = db.Column(db.Integer, primary_key=True)
    patient_id   = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    doctor_id    = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'),   nullable=False)
    diagnosis    = db.Column(db.Text, nullable=False)
    prescription = db.Column(db.Text)
    notes        = db.Column(db.Text)
    date         = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {'record_id':self.record_id,'patient_id':self.patient_id,
                'patient_name':self.patient.name if self.patient else '',
                'doctor_id':self.doctor_id,'doctor_name':self.doctor.name if self.doctor else '',
                'diagnosis':self.diagnosis,'prescription':self.prescription,
                'notes':self.notes,'date':str(self.date)}
