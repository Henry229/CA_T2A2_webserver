from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import OneOf, And, Length
from marshmallow.exceptions import ValidationError

# validation is_admin through Tuple, only can be updated or added by True and False
VALID_IS_ADMIN = (True, False)

# Creating the model of Hrstaff using the SQLAlchemy
class Hrstaff(db.Model):
    __tablename__ = 'hrstaffs'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # setting relationship between hrstaffs and employees. employees is parent and hrstaffs is child
    employees = db.relationship('Employee', back_populates ='hrstaffs', uselist=False)
    
class HrstaffSchema(ma.Schema):
    #employees fields will show all fields of EmployeeSchema except password
    employees = fields.Nested('EmployeeSchema', exclude=['password'])
    # validation of is_admin
    is_admin = fields.Boolean(validate=OneOf(VALID_IS_ADMIN))
    # check the duplicaiton of employee_id
    @validates('employee_id')
    def validate_employee_id(self, value):
        stmt = db.select(Hrstaff).filter_by(employee_id = value)
        employee_id_check = db.session.scalar(stmt)
        if employee_id_check:
            raise ValidationError('You already have the same employee ID')
    class Meta:
        fields = ('id', 'is_admin', 'employees', 'employee_id', 'email')
    