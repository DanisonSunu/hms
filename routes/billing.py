from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.database import db
from models.billing import Billing
from models.patient import Patient

billing_bp = Blueprint('billing', __name__)

@billing_bp.route('/')
@login_required
def list_billing():
    if current_user.role == 'doctor':
        flash('Access denied.', 'warning'); return redirect(url_for('dashboard.index'))
    status_f = request.args.get('status','').strip()
    q = Billing.query
    if status_f: q = q.filter_by(payment_status=status_f)
    bills = q.order_by(Billing.billing_date.desc()).all()
    total_billed  = sum(b.amount for b in Billing.query.all())
    total_paid    = sum(b.amount for b in Billing.query.filter_by(payment_status='Paid').all())
    total_pending = sum(b.amount for b in Billing.query.filter_by(payment_status='Pending').all())
    return render_template('billing/list.html', bills=bills, status_filter=status_f,
                           total_billed=total_billed, total_paid=total_paid, total_pending=total_pending)

@billing_bp.route('/add', methods=['GET','POST'])
@login_required
def add_bill():
    if current_user.role == 'doctor':
        flash('Access denied.', 'danger'); return redirect(url_for('dashboard.index'))
    patients = Patient.query.order_by(Patient.name).all()
    if request.method == 'POST':
        pid=int(request.form.get('patient_id',0)); amount=float(request.form.get('amount',0))
        desc=request.form.get('description','').strip(); ps=request.form.get('payment_status','Pending')
        if not pid or amount <= 0:
            flash('Patient and valid amount required.', 'warning')
            return render_template('billing/add.html', patients=patients)
        b = Billing(patient_id=pid, amount=amount, description=desc, payment_status=ps)
        db.session.add(b); db.session.commit()
        flash(f'Bill of Rs.{amount:.2f} created!', 'success')
        return redirect(url_for('billing.list_billing'))
    return render_template('billing/add.html', patients=patients)

@billing_bp.route('/edit/<int:bill_id>', methods=['GET','POST'])
@login_required
def edit_bill(bill_id):
    if current_user.role == 'doctor':
        flash('Access denied.', 'danger'); return redirect(url_for('dashboard.index'))
    bill = Billing.query.get_or_404(bill_id)
    patients = Patient.query.order_by(Patient.name).all()
    if request.method == 'POST':
        bill.patient_id=int(request.form.get('patient_id',bill.patient_id))
        bill.amount=float(request.form.get('amount',bill.amount))
        bill.description=request.form.get('description',bill.description or '').strip()
        bill.payment_status=request.form.get('payment_status',bill.payment_status)
        db.session.commit(); flash('Bill updated!', 'success')
        return redirect(url_for('billing.list_billing'))
    return render_template('billing/edit.html', bill=bill, patients=patients)

@billing_bp.route('/delete/<int:bill_id>', methods=['POST'])
@login_required
def delete_bill(bill_id):
    if current_user.role != 'admin':
        flash('Admins only.', 'danger'); return redirect(url_for('billing.list_billing'))
    b = Billing.query.get_or_404(bill_id)
    db.session.delete(b); db.session.commit()
    flash('Bill deleted.', 'success')
    return redirect(url_for('billing.list_billing'))

@billing_bp.route('/pay/<int:bill_id>', methods=['POST'])
@login_required
def mark_paid(bill_id):
    if current_user.role == 'doctor':
        return jsonify({'success':False}), 403
    b = Billing.query.get_or_404(bill_id)
    b.payment_status = 'Paid'; db.session.commit()
    return jsonify({'success':True,'status':'Paid','bill_id':bill_id})
