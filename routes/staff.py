from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.database import db
from models.staff import Staff

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/')
@login_required
def list_staff():
    role_f = request.args.get('role','').strip()
    staff_list = Staff.query.filter(Staff.role.ilike(f'%{role_f}%')).all() if role_f else Staff.query.order_by(Staff.name).all()
    roles = sorted(set(s.role for s in Staff.query.all()))
    return render_template('staff/list.html', staff_list=staff_list, roles=roles, role_filter=role_f)

@staff_bp.route('/add', methods=['GET','POST'])
@login_required
def add_staff():
    if current_user.role != 'admin':
        flash('Admins only.', 'danger'); return redirect(url_for('staff.list_staff'))
    if request.method == 'POST':
        m = Staff(name=request.form.get('name','').strip(), role=request.form.get('role','').strip(),
                  phone=request.form.get('phone','').strip(), email=request.form.get('email','').strip() or None,
                  department=request.form.get('department','').strip())
        db.session.add(m); db.session.commit()
        flash(f'Staff "{m.name}" added!', 'success')
        return redirect(url_for('staff.list_staff'))
    return render_template('staff/add.html')

@staff_bp.route('/edit/<int:staff_id>', methods=['GET','POST'])
@login_required
def edit_staff(staff_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger'); return redirect(url_for('staff.list_staff'))
    m = Staff.query.get_or_404(staff_id)
    if request.method == 'POST':
        m.name=request.form.get('name',m.name).strip(); m.role=request.form.get('role',m.role).strip()
        m.phone=request.form.get('phone',m.phone).strip(); m.email=request.form.get('email','').strip() or None
        m.department=request.form.get('department',m.department or '').strip()
        db.session.commit(); flash('Staff updated!', 'success')
        return redirect(url_for('staff.list_staff'))
    return render_template('staff/edit.html', member=m)

@staff_bp.route('/delete/<int:staff_id>', methods=['POST'])
@login_required
def delete_staff(staff_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger'); return redirect(url_for('staff.list_staff'))
    m = Staff.query.get_or_404(staff_id)
    name = m.name; db.session.delete(m); db.session.commit()
    flash(f'Staff "{name}" removed.', 'success')
    return redirect(url_for('staff.list_staff'))
