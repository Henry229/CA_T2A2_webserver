from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError

# Creating the model of employees using the SQLAlchemy
class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    hire_date = db.Column(db.Date)
    salary = db.Column(db.Integer)

    # Creating a foreign key connection to the Job model
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    # Creating a foreign key connection to the Department model
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    
    # setting relationship between jobs and employees. jobs is parent and employees is child
    job = db.relationship('Job', back_populates ='employees')
    # setting relationship between departments and employees. departments is parent and employees is child
    department = db.relationship('Department', back_populates ='employees')
    # setting relationship between departments and employees. employees is parent and hrstaffs is child
    hrstaffs = db.relationship('Hrstaff', back_populates ='employees', uselist=False, cascade='all, delete')
    
    
class EmployeeSchema(ma.Schema):
    # jobs field will show all data of Job entity
    job = fields.Nested('JobSchema')
    # department field will show all data of Department entity 
    department = fields.Nested('DepartmentSchema')
    # validation of email
    email = fields.String(validate=Length(min=2, error='Email must be at least 2 characters long'))
    # validation of name
    name = fields.String(validate=Length(min=2, error='Name must be at least 2 characters long'))
    
    # check the duplication of name 
    @validates('name')
    def validate_name(self, value):
        stmt = db.select(Employee).filter_by(name = value)
        name_check = db.session.scalar(stmt)
        if name_check:
            raise ValidationError('You already have the same name')

    # check the duplication of email 
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
    
    