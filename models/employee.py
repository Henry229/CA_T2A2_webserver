from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100))
    # email = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String)
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
    job = fields.Nested('JobSchema', exclude=['max_salary', 'min_salary'])
    department = fields.Nested('DepartmentSchema')
    # email = fields.String(required=True, validate=Length(min=2, error='Email must be at least 2 characters long'))
    # name = fields.String(required=True, validate=Length(min=2, error='Name must be at least 2 characters long'))
    
    @validates('name')
    def validate_name(self, value):
        stmt = db.select(Employee).filter_by(name = value)
        name_check = db.session.scalar(stmt)
        if name_check:
            raise ValidationError('You already have the same name')

    @validates('email')
    def validate_email(self, value):
        if "@" not in value:
            raise ValidationError('failed email validation')
        stmt = db.select(Employee).filter_by(email = value)
        email_check = db.session.scalar(stmt)
        if email_check:
            raise ValidationError('You already have the same email')
        
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'salary','hire_date', 'job_id', 'department_id', 'job', 'department')
        ordered = True        
    
    