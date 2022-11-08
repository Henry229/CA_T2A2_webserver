from datetime import date
from flask import Blueprint, request, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from flask_jwt_extended import jwt_required
from init import db, bcrypt
from models.job import Job, JobSchema
from models.employee import Employee, EmployeeSchema
from controllers.auth_controller import authorize

job_bp = Blueprint('job', __name__, url_prefix='/job')

@job_bp.route('/')
def job_get_all():
    get_minmax_salary()
    stmt = db.select(Job).order_by(Job.id.asc())
    jobs = db.session.scalars(stmt)
    return JobSchema(many=True).dump(jobs)
  
@job_bp.route('/<int:id>/')
def job_get_one(id):
    stmt = db.select(Job).filter_by(id=id)
    job = db.session.scalar(stmt)
    if job:
        return JobSchema().dump(job)
    else:
        return {'error': f'Job not found with id {id}'}, 404
    

@job_bp.route('/', methods=['POST'])
@jwt_required()
def job_create_one():
    data = JobSchema().load(request.json)
    job = Job(
        job_position = data['job_position'],
    )
    db.session.add(job)
    db.session.commit()
    
    return JobSchema().dump(job), 201
    
@job_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def job_update_one(id):
    authorize()
    stmt = db.select(Job).filter_by(id=id)
    job = db.session.scalar(stmt)
    if job:
        data = JobSchema().load(request.json)
        job.job_position = data('job_position') or job.job_position
        db.session.commit()
        return JobSchema().dump(job)
    else:
        return {'error' : f'Job not found with id {id}'}, 404
    
@job_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def job_delete_one(id):
    authorize()
    stmt = db.select(Job).filter_by(id=id)
    job = db.session.scalar(stmt)
    if job:
        db.session.delete(job)
        db.session.commit()
        return {'message' : f'job id {id} deleted successfully'}
    else:
        return {'error' : f'job not found with id {id}'}
    
def get_minmax_salary():
    # stmt = db.select(Employee.job_id, Job.id, min(Employee.salary), max(Employee.salary)).join(Employee.jobs).group_by(Employee.job_id, Job.id).filter(Employee.job_id == Job.id).order_by(Job.id)
    # stmt = db.select(Employee.job_id, Job.job_position, db.func.min(Employee.salary)).join(Employee.job).group_by(Employee.job_id, Job.job_position).filter(Employee.job_id == Job.id)
    stmt = db.session.query(Employee.job_id, Job.job_position, db.func.min(Employee.salary)).options(joinedload(Employee.job)).group_by(Employee.job_id, Job.job_position).filter(Employee.job_id == Job.id)
    print('@@@@ ', stmt)
    salary = db.session.scalars(stmt)
    for row1 in salary:
        print ('### salary:', row1)
    
    # select a.job_id, b.job_position, min(salary), max(salary) 
    # from employees a, jobs b 
    # where a.job_id = b.id 
    # group by a.job_id, b.job_position 
    # order by a.job_id; 
