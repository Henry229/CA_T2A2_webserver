from datetime import date
from flask import Blueprint, request, abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from init import db, bcrypt
from models.job import Job, JobSchema

job_bp = Blueprint('job', __name__, url_prefix='/job')

@job_bp.route('/')
def job_get_all():
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
def job_create_one():
    try:
        job = Job(
            job_title = request.json['job_title'],
        )
        db.session.add(job)
        db.session.commit()
        
        return JobSchema().dump(job), 201
    except IntegrityError:
        return {'error': 'Data duplicated'}, 409
    
@job_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def job_update_one(id):
    stmt = db.select(Job).filter_by(id=id)
    job = db.session.scalar(stmt)
    if job:
        job.job_title = request.json.get('job_title') or job.job_title
        db.session.commit()
        return JobSchema().dump(job)
    else:
        return {'error' : f'Job not found with id {id}'}, 404
    
@job_bp.route('/<int:id>', methods=['DELETE'])
def job_delete_one(id):
    stmt = db.select(Job).filter_by(id=id)
    job = db.session.scalar(stmt)
    if job:
        db.session.delete(job)
        db.session.commit()
        return {'message' : f'job id {id} deleted successfully'}
    else:
        return {'error' : f'job not found with id {id}'}
