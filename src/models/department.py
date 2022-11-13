from init import db, ma 
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError

#======================================================================= 
# NOTE: Since the department is already a set code, 
# it was limited to only three departments to prevent user input errors. 
# Therefore, the insert and update of the department do not actually work due to validation. 
# I think it is more effective to validate on the frontend page. 
# If the department code is controlled on the frontend page, the statement below can be deleted.
# When updating or adding a department only with endpoint, 
# the values of VALID_DEPARTMENTS must be changed or added.
# Plus, VALID_DEPARTMENTS with comments, I already tested for updating, adding 
# the department works successfully.
#======================================================================= 

VALID_DEPARTMENTS = ('Human Resources', 'IT development', 'Sales')

# Creating the model of Department using the SQLAlchemy
class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String)
    
    # setting relationship between departments and employees. departments is parent and employees is child
    employees = db.relationship('Employee', back_populates ='department', cascade='all, delete')
    
    
class DepartmentSchema(ma.Schema):
    # validation of department_name
    department_name = fields.String(validate=OneOf(VALID_DEPARTMENTS))
    # check the duplication of department_name
    @validates('department_name')
    def validate_department_name(self, value):
        stmt = db.select(Department).filter_by(department_name = value)
        department_check = db.session.scalar(stmt)
        if department_check:
            raise ValidationError('You already have the same department name')
          
    class Meta:
        fields = ('id', 'department_name')
    