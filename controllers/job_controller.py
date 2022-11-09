from datetime import date
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from init import db, bcrypt
from models.job import Job, JobSchema
# from models.employee import Employee, EmployeeSchema
from controllers.auth_controller import authorize

job_bp = Blueprint('job', __name__, url_prefix='/job')

# fetch all instances in jobs table
@job_bp.route('/')
def job_get_all():
    # All instances in jobs table in ascending order of ID
    # select * from jobs
    stmt = db.select(Job).order_by(Job.id.asc())
    jobs = db.session.scalars(stmt)
    # Returning all instances in jobs table wit JobSchema format
    return JobSchema(many=True).dump(jobs)

# fetch an instances in jobs table that you want to retrieve   
@job_bp.route('/<int:id>/')
def job_get_one(id):
    # Get an instance in jobs table matching with parameter id 
    stmt = db.select(Job).filter_by(id=id)
    job = db.session.scalar(stmt)
    if job: # if found
        # Returning an instance in jobs table
        return JobSchema().dump(job)
    else:
        # if not found error 404
        return {'error': f'Job not found with id {id}'}, 404
    
# Create a new job
@job_bp.route('/', methods=['POST'])
# check if HR staff
@jwt_required()
def job_create_one():
    # change request.json to a format of python object
    data = JobSchema().load(request.json)
    job = Job(
        job_position = data['job_position'],
    )
    db.session.add(job)
    db.session.commit()
    # Return successful result with JobSchema format
    return JobSchema().dump(job), 201

# Update information of the jobs table you chose    
@job_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
# check if HR staff
@jwt_required()
def job_update_one(id):
    # check if admin
    authorize()
    # get an instance of jobs table matching with parameter ID 
    # select * from jobs where id = id
    stmt = db.select(Job).filter_by(id=id)
    job = db.session.scalar(stmt)
    if job: # if found
        # change request.json to a format of python object
        data = JobSchema().load(request.json)
        job.job_position = data('job_position') or job.job_position
        db.session.commit()
        # Return successful result with JobSchema format
        return JobSchema().dump(job)
    else:
        # Return not found error 404
        return {'error' : f'Job not found with id {id}'}, 404

# Delete one instance in jobs table that you want to delete  
@job_bp.route('/<int:id>', methods=['DELETE'])
# check if HR staff
@jwt_required()
def job_delete_one(id):
    # check if admin
    authorize()
    # get an instance of jobs table matching with parameter ID 
    # select * from jobs where id = id
    stmt = db.select(Job).filter_by(id=id)
    job = db.session.scalar(stmt)
    if job: # if found
        db.session.delete(job)
        db.session.commit()
        # Return successful result with JobSchema format
        return {'message' : f'job id {id} deleted successfully'}
    else:
        # Return not found error 404
        return {'error' : f'job not found with id {id}'}, 404
    
