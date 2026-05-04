from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.database import db
from models.appointment import Appointment
from models.patient import Patient
from models.doctor import Doctor

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/')
@login_required
def list_appointments():
    status_f = request.args.get('status','').strip()
    q = Appointment.query
    if current_user.role == 'doctor':
        q = q.filter_by(doctor_id=current_user.linked_id)
    if status_f:
        q = q.filter_by(status=status_f)
    appointments = q.order_by(Appointment.date.desc(), Appointment.time).all()
    return render_template('appointments/list.html', appointments=appointments, status_filter=status_f)

@appointments_bp.route('/add', methods=['GET','POST'])
@login_required
def add_appointment():
    if current_user.role == 'doctor':
        flash('Doctors cannot schedule appointments.', 'warning')
        return redirect(url_for('appointments.list_appointments'))
    patients = Patient.query.order_by(Patient.name).all()
    doctors  = Doctor.query.filter_by(available=1).order_by(Doctor.name).all()
    if request.method == 'POST':
        pid=request.form.get('patient_id'); did=request.form.get('doctor_id')
        date=request.form.get('date','').strip(); time=request.form.get('time','').strip()
        notes=request.form.get('notes','').strip()
        if not all([pid,did,date,time]):
            flash('Fill all required fields.', 'warning')
            return render_template('appointments/add.html', patients=patients, doctors=doctors)
        conflict = Appointment.query.filter_by(doctor_id=int(did), date=date, time=time).first()
        if conflict:
            flash(f'Doctor already booked at {time} on {date}.', 'danger')
            return render_template('appointments/add.html', patients=patients, doctors=doctors)
        a = Appointment(patient_id=int(pid), doctor_id=int(did), date=date, time=time, notes=notes)
        db.session.add(a); db.session.commit()
        flash('Appointment scheduled!', 'success')
        return redirect(url_for('appointments.list_appointments'))
    return render_template('appointments/add.html', patients=patients, doctors=doctors)

@appointments_bp.route('/edit/<int:appt_id>', methods=['GET','POST'])
@login_required
def edit_appointment(appt_id):
    if current_user.role == 'doctor':
        flash('Access denied.', 'danger'); return redirect(url_for('appointments.list_appointments'))
    appt = Appointment.query.get_or_404(appt_id)
    patients = Patient.query.order_by(Patient.name).all()
    doctors  = Doctor.query.order_by(Doctor.name).all()
    if request.method == 'POST':
        appt.patient_id=int(request.form.get('patient_id',appt.patient_id))
        appt.doctor_id=int(request.form.get('doctor_id',appt.doctor_id))
        appt.date=request.form.get('date',appt.date); appt.time=request.form.get('time',appt.time)
        appt.status=request.form.get('status',appt.status); appt.notes=request.form.get('notes',appt.notes)
        db.session.commit(); flash('Appointment updated!', 'success')
        return redirect(url_for('appointments.list_appointments'))
    return render_template('appointments/edit.html', appt=appt, patients=patients, doctors=doctors)

@appointments_bp.route('/delete/<int:appt_id>', methods=['POST'])
@login_required
def delete_appointment(appt_id):
    if current_user.role == 'doctor':
        flash('Access denied.', 'danger'); return redirect(url_for('appointments.list_appointments'))
    a = Appointment.query.get_or_404(appt_id)
    db.session.delete(a); db.session.commit()
    flash('Appointment removed.', 'success')
    return redirect(url_for('appointments.list_appointments'))

@appointments_bp.route('/status/<int:appt_id>', methods=['POST'])
@login_required
def update_status(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    data = request.get_json()
    new_status = data.get('status','')
    if new_status in ('Scheduled','Completed','Cancelled'):
        appt.status = new_status; db.session.commit()
        return jsonify({'success':True,'status':new_status})
    return jsonify({'success':False}), 400
