from models.database import db

class Billing(db.Model):
    __tablename__ = 'billing'
    bill_id        = db.Column(db.Integer, primary_key=True)
    patient_id     = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    amount         = db.Column(db.Float,   nullable=False)
    description    = db.Column(db.Text)
    payment_status = db.Column(db.String(20), default='Pending')
    billing_date   = db.Column(db.DateTime,   server_default=db.func.now())

    def to_dict(self):
        return {'bill_id':self.bill_id,'patient_id':self.patient_id,
                'patient_name':self.patient.name if self.patient else '',
                'amount':self.amount,'description':self.description,
                'payment_status':self.payment_status,'billing_date':str(self.billing_date)}
