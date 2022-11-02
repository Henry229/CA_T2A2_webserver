from init import db, ma 

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String)
    # manager_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    # manages = db.relationship('Employee', back_populates ='department')
    
    employees = db.relationship('Employee', back_populates ='department', cascade='all, delete')
    
class DepartmentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'department_name')
    