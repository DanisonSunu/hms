from models.database import db

class Inventory(db.Model):
    __tablename__ = 'inventory'
    item_id      = db.Column(db.Integer,     primary_key=True)
    item_name    = db.Column(db.String(150), nullable=False)
    category     = db.Column(db.String(50))
    quantity     = db.Column(db.Integer,     nullable=False, default=0)
    unit         = db.Column(db.String(30),  default='units')
    supplier     = db.Column(db.String(150))
    unit_price   = db.Column(db.Float,       default=0.0)
    last_updated = db.Column(db.DateTime,    server_default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {'item_id':self.item_id,'item_name':self.item_name,'category':self.category,
                'quantity':self.quantity,'unit':self.unit,'supplier':self.supplier,
                'unit_price':self.unit_price,'last_updated':str(self.last_updated)}
