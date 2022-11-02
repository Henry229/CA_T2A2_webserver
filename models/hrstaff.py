from init import db, ma

class Hrstaff(db.Model):
    __tablename__ = 'hrstaffs'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    employees = db.relationship('Employee', back_populates ='hrstaffs')
    
class HrstaffSchema(ma.Schema):
    class Meta:
        fields = ('id', 'is_admin')
    