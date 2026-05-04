from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.database import db
from models.record import MedicalRecord
from models.patient import Patient
from models.doctor import Doctor

records_bp = Blueprint('records', __name__)

@records_bp.route('/')
@login_required
def list_records():
    if current_user.role == 'staff':
        flash('Access denied.', 'warning'); return redirect(url_for('dashboard.index'))
    q = MedicalRecord.query
    if current_user.role == 'doctor':
        q = q.filter_by(doctor_id=current_user.linked_id)
    search = request.args.get('search','').strip()
    if search:
        pids = [p.patient_id for p in Patient.query.filter(Patient.name.ilike(f'%{search}%')).all()]
        q = q.filter(MedicalRecord.patient_id.in_(pids))
    records = q.order_by(MedicalRecord.date.desc()).all()
    return render_template('records/list.html', records=records, search=search)

@records_bp.route('/add', methods=['GET','POST'])
@login_required
def add_record():
    if current_user.role == 'staff':
        flash('Access denied.', 'danger'); return redirect(url_for('dashboard.index'))
    patients = Patient.query.order_by(Patient.name).all()
    doctors  = Doctor.query.order_by(Doctor.name).all()
    if request.method == 'POST':
        pid=int(request.form.get('patient_id',0)); did=int(request.form.get('doctor_id',0))
        diagnosis=request.form.get('diagnosis','').strip()
        prescription=request.form.get('prescription','').strip()
        notes=request.form.get('notes','').strip()
        if not pid or not did or not diagnosis:
            flash('Patient, doctor and diagnosis required.', 'warning')
            return render_template('records/add.html', patients=patients, doctors=doctors)
        r = MedicalRecord(patient_id=pid, doctor_id=did, diagnosis=diagnosis, prescription=prescription, notes=notes)
        db.session.add(r); db.session.commit()
        flash('Medical record created!', 'success')
        return redirect(url_for('records.list_records'))
    return render_template('records/add.html', patients=patients, doctors=doctors)

@records_bp.route('/<int:record_id>')
@login_required
def view_record(record_id):
    if current_user.role == 'staff':
        flash('Access denied.', 'danger'); return redirect(url_for('dashboard.index'))
    return render_template('records/detail.html', record=MedicalRecord.query.get_or_404(record_id))

@records_bp.route('/edit/<int:record_id>', methods=['GET','POST'])
@login_required
def edit_record(record_id):
    if current_user.role == 'staff':
        flash('Access denied.', 'danger'); return redirect(url_for('dashboard.index'))
    record = MedicalRecord.query.get_or_404(record_id)
    patients = Patient.query.order_by(Patient.name).all()
    doctors  = Doctor.query.order_by(Doctor.name).all()
    if request.method == 'POST':
        record.patient_id=int(request.form.get('patient_id',record.patient_id))
        record.doctor_id=int(request.form.get('doctor_id',record.doctor_id))
        record.diagnosis=request.form.get('diagnosis',record.diagnosis).strip()
        record.prescription=request.form.get('prescription',record.prescription or '').strip()
        record.notes=request.form.get('notes',record.notes or '').strip()
        db.session.commit(); flash('Record updated!', 'success')
        return redirect(url_for('records.view_record', record_id=record_id))
    return render_template('records/edit.html', record=record, patients=patients, doctors=doctors)

@records_bp.route('/delete/<int:record_id>', methods=['POST'])
@login_required
def delete_record(record_id):
    if current_user.role != 'admin':
        flash('Admins only.', 'danger'); return redirect(url_for('records.list_records'))
    r = MedicalRecord.query.get_or_404(record_id)
    db.session.delete(r); db.session.commit()
    flash('Record deleted.', 'success')
    return redirect(url_for('records.list_records'))
