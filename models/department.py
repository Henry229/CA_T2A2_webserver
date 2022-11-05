from init import db, ma 
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError

VALID_DEPARTMENTS = ('Human Resources', 'IT development', 'Sales')

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String)
    
    employees = db.relationship('Employee', back_populates ='department', cascade='all, delete')
    
    
class DepartmentSchema(ma.Schema):
    department_name = fields.String(required=True, validate=OneOf(VALID_DEPARTMENTS))
    @validates('department_name')
    def validate_department_name(self, value):
        stmt = db.select(Department).filter_by(department_name = value)
        department_check = db.session.scalar(stmt)
        if department_check:
            raise ValidationError('You already have the same department name')
          
    class Meta:
        fields = ('id', 'department_name')
    