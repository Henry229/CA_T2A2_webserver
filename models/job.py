from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError

VALID_JOBPOSTION = ('Junior', 'IT Senior', 'Lead', 'Manager', 'Director', 'CEO')


class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    job_position = db.Column(db.String)
    # min_salary = db.Column(db.Integer)
    # max_salary = db.Column(db.Integer)
    
    employees = db.relationship('Employee', back_populates ='job', cascade='all, delete')
    
class JobSchema(ma.Schema):
    job_position = fields.String(required=True, validate=OneOf(VALID_JOBPOSTION))

    @validates('job_position')
    def validate_job_position(self, value):
        stmt = db.select(Job).filter_by(job_position = value)
        job_check = db.session.scalar(stmt)
        if job_check:
            raise ValidationError('You already have the same job position name')
    class Meta:
        fields = ('id', 'job_position', 'min_salary', 'max_salary')
    