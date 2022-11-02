from datetime import date
from flask import Blueprint, request, abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from init import db, bcrypt
from models.employee import Employee, EmployeeSchema

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
        employee = Employee(
            email = request.json['email'],
            name = request.json['name'],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8'),
            hire_date = date.today(),
            salary = request.json['salary'],
            job_id = request.json['job_id'],
            department_id = request.json['department_id']
        )
        db.session.add(employee)
        db.session.commit()
        
        return EmployeeSchema(exclude=['password']).dump(employee), 201
    except IntegrityError:
        return {'error': 'Email address already exists'}, 409
    
@employee_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def employee_update_one(id):
    stmt = db.select(Employee).filter_by(id=id)
    employee = db.session.scalar(stmt)
    if employee:
        employee.email = request.json.get('email') or employee.email,
        employee.name = request.json.get('name') or employee.name,
        employee.hire_date = request.json.get('hire_date') or employee.hire_date,
        employee.salary = request.json.get('salary') or employee.salary
        db.session.commit()
        return EmployeeSchema(exclude=['password']).dump(employee)
    else:
        return {'error' : f'Employee not found with id {id}'}, 404
    
@employee_bp.route('/<int:id>', methods=['DELETE'])
def employee_delete_one(id):
    stmt = db.select(Employee).filter_by(id=id)
    employee = db.session.scalar(stmt)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return {'message' : f'Employee id {id} deleted successfully'}
    else:
        return {'error' : f'Employee not found with id {id}'}
