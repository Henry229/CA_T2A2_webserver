from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError

#======================================================================= 
# NOTE: Since the jobs table is already a set code, 
# it was limited to only six jobs to prevent user input errors
# because code table is a critical table to handle the whole system. 
# Therefore, the insert and update of the job_position do not actually work due to validation. 
# I think it is more effective to validate it on the frontend page. 
# If the job_position code is controlled on the frontend page, the statement below can be deleted.
# When updating or adding a job_position only with endpoint, 
# the values of VALID_JOBPOSITION must be changed or added.
# Plus, VALID_JOBPOSITION with comments, I already tested for updating, adding 
# the job_position works successfully.
#======================================================================= 

VALID_JOBPOSTION = ('Junior', 'Senior', 'Lead', 'Manager', 'Director', 'CEO')

# Creating the model of Job using the SQLAlchemy
class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    job_position = db.Column(db.String)
    
    # setting relationship between jobs and employees. jobs is parent and employees is child
    employees = db.relationship('Employee', back_populates ='job', cascade='all, delete')
    
class JobSchema(ma.Schema):
    # validation of job_position
    job_position = fields.String(required=True, validate=OneOf(VALID_JOBPOSTION))

    # check teh duplication of job_position
    @validates('job_position')
    def validate_job_position(self, value):
        stmt = db.select(Job).filter_by(job_position = value)
        job_check = db.session.scalar(stmt)
        if job_check:
            raise ValidationError('You already have the same job position name')
    class Meta:
        fields = ('id', 'job_position')
    