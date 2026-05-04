"""
Hospital Management System - app.py
Main Flask application factory.
Run: python app.py
Default credentials:
  admin   / admin123
  doctor1 / doctor123
  staff1  / staff123
"""
from flask import Flask
from flask_login import LoginManager
from models.database import db
from models.user import User
from routes.auth         import auth_bp
from routes.patients     import patients_bp
from routes.doctors      import doctors_bp
from routes.staff        import staff_bp
from routes.appointments import appointments_bp
from routes.records      import records_bp
from routes.billing      import billing_bp
from routes.inventory    import inventory_bp
from routes.dashboard    import dashboard_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hms-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hms.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp,         url_prefix='/auth')
    app.register_blueprint(dashboard_bp,    url_prefix='/')
    app.register_blueprint(patients_bp,     url_prefix='/patients')
    app.register_blueprint(doctors_bp,      url_prefix='/doctors')
    app.register_blueprint(staff_bp,        url_prefix='/staff')
    app.register_blueprint(appointments_bp, url_prefix='/appointments')
    app.register_blueprint(records_bp,      url_prefix='/records')
    app.register_blueprint(billing_bp,      url_prefix='/billing')
    app.register_blueprint(inventory_bp,    url_prefix='/inventory')

    with app.app_context():
        db.create_all()
        seed_database()

    return app

def seed_database():
    from models.user       import User
    from models.patient    import Patient
    from models.doctor     import Doctor
    from models.staff      import Staff
    from models.appointment import Appointment
    from models.record     import MedicalRecord
    from models.billing    import Billing
    from models.inventory  import Inventory
    from werkzeug.security import generate_password_hash

    if User.query.count() > 0:
        return

    print("[HMS] Seeding database...")

    doctors = [
        Doctor(name='Dr. Arjun Mehta',   specialization='Cardiology',  phone='9876543210', email='arjun@hms.com',   experience=12),
        Doctor(name='Dr. Priya Sharma',  specialization='Neurology',   phone='9876543211', email='priya@hms.com',   experience=8),
        Doctor(name='Dr. Ravi Kumar',    specialization='Orthopedics', phone='9876543212', email='ravi@hms.com',    experience=15),
        Doctor(name='Dr. Sunita Nair',   specialization='Pediatrics',  phone='9876543213', email='sunita@hms.com',  experience=6),
        Doctor(name='Dr. Anil Verma',    specialization='Dermatology', phone='9876543214', email='anil@hms.com',    experience=10),
    ]
    db.session.add_all(doctors)

    staff_list = [
        Staff(name='Kavya Reddy',   role='Nurse',          phone='9123456780', email='kavya@hms.com',   department='General Ward'),
        Staff(name='Mohan Das',     role='Receptionist',   phone='9123456781', email='mohan@hms.com',   department='Front Desk'),
        Staff(name='Lakshmi Iyer',  role='Lab Technician', phone='9123456782', email='lakshmi@hms.com', department='Pathology'),
        Staff(name='Suresh Pillai', role='Pharmacist',     phone='9123456783', email='suresh@hms.com',  department='Pharmacy'),
    ]
    db.session.add_all(staff_list)

    patients = [
        Patient(name='Ramesh Nair',    age=45, gender='Male',   phone='8888888881', address='Kochi, Kerala',      blood_group='B+'),
        Patient(name='Meena Krishnan', age=32, gender='Female', phone='8888888882', address='Thrissur, Kerala',   blood_group='O+'),
        Patient(name='Ajith Kumar',    age=58, gender='Male',   phone='8888888883', address='Kozhikode, Kerala',  blood_group='A+'),
        Patient(name='Divya Menon',    age=27, gender='Female', phone='8888888884', address='Trivandrum, Kerala', blood_group='AB+'),
        Patient(name='George Thomas',  age=70, gender='Male',   phone='8888888885', address='Kottayam, Kerala',   blood_group='O-'),
    ]
    db.session.add_all(patients)
    db.session.flush()

    users = [
        User(username='admin',   password=generate_password_hash('admin123'),  role='admin'),
        User(username='doctor1', password=generate_password_hash('doctor123'), role='doctor', linked_id=1),
        User(username='staff1',  password=generate_password_hash('staff123'),  role='staff',  linked_id=1),
    ]
    db.session.add_all(users)

    appointments = [
        Appointment(patient_id=1, doctor_id=1, date='2025-07-10', time='09:00', status='Scheduled'),
        Appointment(patient_id=2, doctor_id=2, date='2025-07-10', time='10:30', status='Scheduled'),
        Appointment(patient_id=3, doctor_id=3, date='2025-07-11', time='14:00', status='Completed'),
        Appointment(patient_id=4, doctor_id=4, date='2025-07-12', time='11:00', status='Scheduled'),
        Appointment(patient_id=5, doctor_id=1, date='2025-07-09', time='16:00', status='Completed'),
    ]
    db.session.add_all(appointments)

    records = [
        MedicalRecord(patient_id=3, doctor_id=3, diagnosis='Knee Osteoarthritis',
                      prescription='Ibuprofen 400mg, Calcium supplements', notes='Follow-up in 2 weeks'),
        MedicalRecord(patient_id=5, doctor_id=1, diagnosis='Hypertension Stage 2',
                      prescription='Amlodipine 5mg, Losartan 50mg',      notes='Low salt diet recommended'),
    ]
    db.session.add_all(records)

    bills = [
        Billing(patient_id=1, amount=1500.00, description='Consultation + ECG',           payment_status='Pending'),
        Billing(patient_id=2, amount=2200.00, description='Neurology Consultation + MRI',  payment_status='Paid'),
        Billing(patient_id=3, amount=3500.00, description='Orthopedic Surgery Prep',       payment_status='Paid'),
        Billing(patient_id=4, amount=800.00,  description='Pediatric Consultation',        payment_status='Pending'),
        Billing(patient_id=5, amount=2800.00, description='Cardiac Checkup Package',       payment_status='Paid'),
    ]
    db.session.add_all(bills)

    items = [
        Inventory(item_name='Paracetamol 500mg', category='Medicine',   quantity=500,  unit='tablets', supplier='MedPlus Pharma',     unit_price=0.50),
        Inventory(item_name='Ibuprofen 400mg',   category='Medicine',   quantity=300,  unit='tablets', supplier='Sun Pharma',          unit_price=0.75),
        Inventory(item_name='Surgical Gloves',   category='Consumable', quantity=1000, unit='pairs',   supplier='HealthCare Supplies', unit_price=12.00),
        Inventory(item_name='Syringes 5ml',      category='Consumable', quantity=800,  unit='units',   supplier='BD Medical',          unit_price=2.50),
        Inventory(item_name='BP Monitor',        category='Equipment',  quantity=10,   unit='units',   supplier='Omron India',         unit_price=2500.00),
        Inventory(item_name='Pulse Oximeter',    category='Equipment',  quantity=15,   unit='units',   supplier='Nonin Medical',       unit_price=800.00),
        Inventory(item_name='Hand Sanitizer',    category='Consumable', quantity=200,  unit='bottles', supplier='Dettol',              unit_price=85.00),
        Inventory(item_name='IV Cannula 18G',    category='Consumable', quantity=600,  unit='units',   supplier='BD Medical',          unit_price=8.00),
    ]
    db.session.add_all(items)
    db.session.commit()
    print("[HMS] Seeding complete.")

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
