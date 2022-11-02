from datetime import date
from flask import Blueprint, request, abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from init import db, bcrypt
from models.department import Department, DepartmentSchema

department_bp = Blueprint('department', __name__, url_prefix='/department')

@department_bp.route('/')
def department_get_all():
    stmt = db.select(Department).order_by(Department.id.asc())
    departments = db.session.scalars(stmt)
    return DepartmentSchema(many=True).dump(departments)
  
@department_bp.route('/<int:id>/')
def department_get_one(id):
    stmt = db.select(Department).filter_by(id=id)
    department = db.session.scalar(stmt)
    if department:
        return DepartmentSchema().dump(department)
    else:
        return {'error': f'Department not found with id {id}'}, 404
    

@department_bp.route('/', methods=['POST'])
def department_create_one():
    try:
        department = Department(
            department_name = request.json['department_name'],
        )
        db.session.add(department)
        db.session.commit()
        
        return DepartmentSchema().dump(department), 201
    except IntegrityError:
        return {'error': 'Data duplicated'}, 409
    
@department_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def department_update_one(id):
    stmt = db.select(Department).filter_by(id=id)
    department = db.session.scalar(stmt)
    if department:
        department.department_name = request.json.get('department_name') or department.department_name,
        db.session.commit()
        return DepartmentSchema().dump(department)
    else:
        return {'error' : f'Employee not found with id {id}'}, 404
    
@department_bp.route('/<int:id>', methods=['DELETE'])
def department_delete_one(id):
    stmt = db.select(Department).filter_by(id=id)
    department = db.session.scalar(stmt)
    if department:
        db.session.delete(department)
        db.session.commit()
        return {'message' : f'Department id {id} deleted successfully'}
    else:
        return {'error' : f'Department not found with id {id}'}
