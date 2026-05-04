from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.database import db
from models.patient import Patient

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/')
@login_required
def list_patients():
    search = request.args.get('search','').strip()
    if search:
        patients = Patient.query.filter(
            (Patient.name.ilike(f'%{search}%')) | (Patient.phone.ilike(f'%{search}%'))
        ).order_by(Patient.registration_date.desc()).all()
    else:
        patients = Patient.query.order_by(Patient.registration_date.desc()).all()
    return render_template('patients/list.html', patients=patients, search=search)

@patients_bp.route('/add', methods=['GET','POST'])
@login_required
def add_patient():
    if current_user.role not in ('admin','staff'):
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard.index'))
    if request.method == 'POST':
        name=request.form.get('name','').strip(); age=request.form.get('age',0)
        gender=request.form.get('gender',''); phone=request.form.get('phone','').strip()
        address=request.form.get('address','').strip(); blood_group=request.form.get('blood_group','').strip()
        if not name or not age or not gender or not phone:
            flash('Fill all required fields.', 'warning')
            return render_template('patients/add.html')
        p = Patient(name=name, age=int(age), gender=gender, phone=phone, address=address, blood_group=blood_group)
        db.session.add(p); db.session.commit()
        flash(f'Patient "{name}" registered!', 'success')
        return redirect(url_for('patients.list_patients'))
    return render_template('patients/add.html')

@patients_bp.route('/<int:patient_id>')
@login_required
def view_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template('patients/detail.html', patient=patient)

@patients_bp.route('/edit/<int:patient_id>', methods=['GET','POST'])
@login_required
def edit_patient(patient_id):
    if current_user.role not in ('admin','staff'):
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard.index'))
    patient = Patient.query.get_or_404(patient_id)
    if request.method == 'POST':
        patient.name=request.form.get('name',patient.name).strip()
        patient.age=int(request.form.get('age',patient.age))
        patient.gender=request.form.get('gender',patient.gender)
        patient.phone=request.form.get('phone',patient.phone).strip()
        patient.address=request.form.get('address',patient.address or '').strip()
        patient.blood_group=request.form.get('blood_group',patient.blood_group or '').strip()
        db.session.commit(); flash('Patient updated!', 'success')
        return redirect(url_for('patients.view_patient', patient_id=patient_id))
    return render_template('patients/edit.html', patient=patient)

@patients_bp.route('/delete/<int:patient_id>', methods=['POST'])
@login_required
def delete_patient(patient_id):
    if current_user.role != 'admin':
        flash('Admins only.', 'danger')
        return redirect(url_for('patients.list_patients'))
    p = Patient.query.get_or_404(patient_id)
    name = p.name; db.session.delete(p); db.session.commit()
    flash(f'Patient "{name}" removed.', 'success')
    return redirect(url_for('patients.list_patients'))

@patients_bp.route('/api/all')
@login_required
def api_all_patients():
    return jsonify([p.to_dict() for p in Patient.query.order_by(Patient.name).all()])
