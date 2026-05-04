from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.patient import Patient
from models.doctor import Doctor
from models.staff import Staff
from models.appointment import Appointment
from models.billing import Billing
from models.inventory import Inventory
from models.record import MedicalRecord

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    stats = {
        'total_patients':         Patient.query.count(),
        'total_doctors':          Doctor.query.count(),
        'total_staff':            Staff.query.count(),
        'total_appointments':     Appointment.query.count(),
        'scheduled_appointments': Appointment.query.filter_by(status='Scheduled').count(),
        'total_records':          MedicalRecord.query.count(),
        'pending_bills':          Billing.query.filter_by(payment_status='Pending').count(),
        'total_revenue':          sum(b.amount for b in Billing.query.filter_by(payment_status='Paid').all()),
        'low_stock_items':        Inventory.query.filter(Inventory.quantity < 50).count(),
    }
    recent_appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(5).all()
    return render_template('dashboard.html', stats=stats, recent_appointments=recent_appointments)
