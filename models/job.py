from init import db, ma 

class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String)
    min_salary = db.Column(db.Integer)
    max_salary = db.Column(db.Integer)
    
    employees = db.relationship('Employee', back_populates ='job', cascade='all, delete')
    
class JobSchema(ma.Schema):
    class Meta:
        fields = ('id', 'job_title', 'min_salary', 'max_salary')
    