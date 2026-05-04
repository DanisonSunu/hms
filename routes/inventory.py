from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.database import db
from models.inventory import Inventory

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/')
@login_required
def list_inventory():
    if current_user.role == 'doctor':
        flash('Access denied.', 'warning'); return redirect(url_for('dashboard.index'))
    cat_f = request.args.get('category','').strip()
    q = Inventory.query
    if cat_f: q = q.filter_by(category=cat_f)
    items = q.order_by(Inventory.item_name).all()
    categories = sorted(set(i.category for i in Inventory.query.all() if i.category))
    return render_template('inventory/list.html', items=items, categories=categories, category_filter=cat_f)

@inventory_bp.route('/add', methods=['GET','POST'])
@login_required
def add_item():
    if current_user.role != 'admin':
        flash('Admins only.', 'danger'); return redirect(url_for('inventory.list_inventory'))
    if request.method == 'POST':
        item = Inventory(item_name=request.form.get('item_name','').strip(),
                         category=request.form.get('category','').strip(),
                         quantity=int(request.form.get('quantity',0)),
                         unit=request.form.get('unit','units').strip(),
                         supplier=request.form.get('supplier','').strip(),
                         unit_price=float(request.form.get('unit_price',0.0)))
        db.session.add(item); db.session.commit()
        flash(f'Item "{item.item_name}" added!', 'success')
        return redirect(url_for('inventory.list_inventory'))
    return render_template('inventory/add.html')

@inventory_bp.route('/edit/<int:item_id>', methods=['GET','POST'])
@login_required
def edit_item(item_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger'); return redirect(url_for('inventory.list_inventory'))
    item = Inventory.query.get_or_404(item_id)
    if request.method == 'POST':
        item.item_name=request.form.get('item_name',item.item_name).strip()
        item.category=request.form.get('category',item.category or '').strip()
        item.quantity=int(request.form.get('quantity',item.quantity))
        item.unit=request.form.get('unit',item.unit).strip()
        item.supplier=request.form.get('supplier',item.supplier or '').strip()
        item.unit_price=float(request.form.get('unit_price',item.unit_price))
        db.session.commit(); flash('Item updated!', 'success')
        return redirect(url_for('inventory.list_inventory'))
    return render_template('inventory/edit.html', item=item)

@inventory_bp.route('/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger'); return redirect(url_for('inventory.list_inventory'))
    item = Inventory.query.get_or_404(item_id)
    name = item.item_name; db.session.delete(item); db.session.commit()
    flash(f'Item "{name}" removed.', 'success')
    return redirect(url_for('inventory.list_inventory'))

@inventory_bp.route('/restock/<int:item_id>', methods=['POST'])
@login_required
def restock_item(item_id):
    if current_user.role != 'admin':
        return jsonify({'success':False}), 403
    item = Inventory.query.get_or_404(item_id)
    data = request.get_json()
    qty = int(data.get('quantity',0))
    if qty <= 0: return jsonify({'success':False,'error':'Qty must be > 0'}), 400
    item.quantity += qty; db.session.commit()
    return jsonify({'success':True,'new_quantity':item.quantity})
