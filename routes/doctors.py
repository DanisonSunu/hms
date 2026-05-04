from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.database import db
from models.doctor import Doctor

doctors_bp = Blueprint('doctors', __name__)

@doctors_bp.route('/')
@login_required
def list_doctors():
    spec = request.args.get('specialization','').strip()
    doctors = Doctor.query.filter(Doctor.specialization.ilike(f'%{spec}%')).all() if spec else Doctor.query.order_by(Doctor.name).all()
    specializations = sorted(set(d.specialization for d in Doctor.query.all()))
    return render_template('doctors/list.html', doctors=doctors, specializations=specializations, spec_filter=spec)

@doctors_bp.route('/add', methods=['GET','POST'])
@login_required
def add_doctor():
    if current_user.role != 'admin':
        flash('Admins only.', 'danger'); return redirect(url_for('doctors.list_doctors'))
    if request.method == 'POST':
        d = Doctor(name=request.form.get('name','').strip(),
                   specialization=request.form.get('specialization','').strip(),
                   phone=request.form.get('phone','').strip(),
                   email=request.form.get('email','').strip() or None,
                   experience=int(request.form.get('experience',0)),
                   available=1 if request.form.get('available') else 0)
        db.session.add(d); db.session.commit()
        flash(f'Doctor "{d.name}" added!', 'success')
        return redirect(url_for('doctors.list_doctors'))
    return render_template('doctors/add.html')

@doctors_bp.route('/edit/<int:doctor_id>', methods=['GET','POST'])
@login_required
def edit_doctor(doctor_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger'); return redirect(url_for('doctors.list_doctors'))
    doctor = Doctor.query.get_or_404(doctor_id)
    if request.method == 'POST':
        doctor.name=request.form.get('name',doctor.name).strip()
        doctor.specialization=request.form.get('specialization',doctor.specialization).strip()
        doctor.phone=request.form.get('phone',doctor.phone).strip()
        doctor.email=request.form.get('email','').strip() or None
        doctor.experience=int(request.form.get('experience',doctor.experience))
        doctor.available=1 if request.form.get('available') else 0
        db.session.commit(); flash('Doctor updated!', 'success')
        return redirect(url_for('doctors.list_doctors'))
    return render_template('doctors/edit.html', doctor=doctor)

@doctors_bp.route('/delete/<int:doctor_id>', methods=['POST'])
@login_required
def delete_doctor(doctor_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger'); return redirect(url_for('doctors.list_doctors'))
    d = Doctor.query.get_or_404(doctor_id)
    name = d.name; db.session.delete(d); db.session.commit()
    flash(f'Doctor "{name}" removed.', 'success')
    return redirect(url_for('doctors.list_doctors'))

@doctors_bp.route('/api/all')
@login_required
def api_all_doctors():
    return jsonify([d.to_dict() for d in Doctor.query.filter_by(available=1).order_by(Doctor.name).all()])
