from init import db, ma

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    hire_date = db.Column(db.Date)
    salary = db.Column(db.Integer)

    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    # manager_id = db.Column(db.Integer, db.ForeignKey('managements.id'), nullable=False)
    
    job = db.relationship('Job', back_populates ='employees')
    department = db.relationship('Department', back_populates ='employees')
    
    hrstaffs = db.relationship('Hrstaff', back_populates ='employees', cascade='all, delete')
    
    
class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'salary','hire_date')
        ordered = True        
    
    