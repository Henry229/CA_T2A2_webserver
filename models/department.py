from init import db, ma 
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError

VALID_DEPARTMENTS = ('Human Resources', 'IT development', 'Sales')

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String)
    # manager_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    # manages = db.relationship('Employee', back_populates ='department')
    
    employees = db.relationship('Employee', back_populates ='department', cascade='all, delete')
    
    
class DepartmentSchema(ma.Schema):
    department_name = fields.String(required=True, Validate=OneOf(VALID_DEPARTMENTS))
    class Meta:
        fields = ('id', 'department_name')
    