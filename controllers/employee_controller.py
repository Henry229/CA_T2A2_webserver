from datetime import date
from flask import Blueprint, request, abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from init import db, bcrypt
from models.employee import Employee, EmployeeSchema
from controllers.auth_controller import authorize

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')

@employee_bp.route('/')
def employee_get_employees():
    stmt = db.select(Employee).order_by(Employee.id.asc())
    employees = db.session.scalars(stmt)
    return EmployeeSchema(many=True, exclude=['password']).dump(employees)
  
@employee_bp.route('/<int:id>/')
def employee_get_one(id):
    stmt = db.select(Employee).filter_by(id=id)
    employee = db.session.scalar(stmt)
    if employee:
        return EmployeeSchema(exclude=['password']).dump(employee)
    else:
        return {'error': f'Employee not found with id {id}'}, 404
    

@employee_bp.route('/', methods=['POST'])
@jwt_required()
def employee_create_one():
    try:
        data = EmployeeSchema().load(request.json)
        employee = Employee(
            email = data['email'],
            name = data['name'],
            password = bcrypt.generate_password_hash(data['password']).decode('utf-8'),
            hire_date = date.today(),
            salary = data['salary'],
            job_id = data['job_id'],
            department_id = data['department_id']
        )
        db.session.add(employee)
        db.session.commit()
        
        return EmployeeSchema(exclude=['password']).dump(employee), 201
    except IntegrityError:
        return {'error': 'Email address already exists'}, 409
    
@employee_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def employee_update_one(id):
    authorize()
    stmt = db.select(Employee).filter_by(id=id)
    employee = db.session.scalar(stmt)
    if employee:
        data = EmployeeSchema().load(request.json)
                
        employee.email = data.get('email') or employee.email
        employee.name = data.get('name') or employee.name
        employee.hire_date = data.get('hire_date') or employee.hire_date
        employee.salary = data.get('salary') or employee.salary
        employee.job_id = data.get('job_id') or employee.job_id
        employee.department_id = data.get('department_id') or employee.department_id
        db.session.commit()
        return EmployeeSchema(exclude=['password']).dump(employee)
    else:
        return {'error' : f'Employee not found with id {id}'}, 404
    
@employee_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def employee_delete_one(id):
    authorize()
    stmt = db.select(Employee).filter_by(id=id)
    employee = db.session.scalar(stmt)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return {'message' : f'Employee id {id} deleted successfully'}
    else:
        return {'error' : f'Employee not found with id {id}'}
