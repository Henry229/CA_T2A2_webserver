from init import db, ma 

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String)
    manager_id = db.Column(db.Integer)
    
class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'department_name')
    