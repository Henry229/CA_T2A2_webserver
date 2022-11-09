from datetime import date
from flask import Blueprint, request, abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import get_jwt_identity, jwt_required
from init import db, bcrypt
from models.department import Department, DepartmentSchema
from controllers.auth_controller import authorize

department_bp = Blueprint('department', __name__, url_prefix='/department')

#fatch all instances in departments table 
@department_bp.route('/')
def department_get_all():
    # All instances in departments table in ascending order of ID
    # select * from departments;
    stmt = db.select(Department).order_by(Department.id.asc())
    departments = db.session.scalars(stmt)
    # Returning all instances in departments table with DepartmentSchema format
    return DepartmentSchema(many=True).dump(departments)

# fetch an instance from departments table that you want to retrieve
@department_bp.route('/<int:id>/')
def department_get_one(id):
    # Get an instance from departments table matching with parameter id
    stmt = db.select(Department).filter_by(id=id)
    department = db.session.scalar(stmt)
    if department: # if found
        # Returning an instance from department table
        return DepartmentSchema().dump(department)
    else:
        # if not found department id return 404 error
        return {'error': f'Department not found with id {id}'}, 404
    
# Create a new department
@department_bp.route('/', methods=['POST'])
# check if HR staff
@jwt_required()
def department_create_one():
    # Using try: except: if a new department added is already in departments table 
    try:
        # change request.json to a format of python object
        data = DepartmentSchema().load(request.json)
        department = Department(
            department_name = data['department_name'],
        )
        db.session.add(department)
        db.session.commit()
        # Return successful result with format of DepartmentSchema
        return DepartmentSchema().dump(department), 201
    except IntegrityError:
        # Returning 409 error 
        return {'error': 'Data duplicated'}, 409
    
# Update information of the departments table you chose 
@department_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
# check if HR staff
@jwt_required()
def department_update_one(id):
    # check if admin
    authorize()
    # get an instance of department table matching with parameter ID 
    # select * from departments where id = id
    stmt = db.select(Department).filter_by(id=id)
    department = db.session.scalar(stmt)
    if department: # if found
        # change request.json to a format of python object
        data = DepartmentSchema().load(request.json)
        
        department.department_name = data.get('department_name') or department.department_name,
        db.session.commit()
        # Return successful result for update with format of DepartmentSchema
        return DepartmentSchema().dump(department)
    else:
        # Returning not found error 404 
        return {'error' : f'Employee not found with id {id}'}, 404

# Delete one instance in departments table that you want to delete
@department_bp.route('/<int:id>', methods=['DELETE'])
# check if HR staff
@jwt_required()
def department_delete_one(id):
    # if admin 
    authorize()
    # get an instance of departments table matching with parameter ID 
    # select * from departments where id = id
    stmt = db.select(Department).filter_by(id=id)
    department = db.session.scalar(stmt)
    if department: # if found
        db.session.delete(department)
        db.session.commit()
        # Returning successful message when deleted
        return {'message' : f'Department id {id} deleted successfully'}
    else:
        # Returning not found error 404
        return {'error' : f'Department not found with id {id}'}, 404
