from datetime import date
from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required
from init import db, bcrypt
from models.employee import Employee, EmployeeSchema
from controllers.auth_controller import authorize

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')

# fetch all instances in employees table 
@employee_bp.route('/')
def employee_get_employees():
    # All instances in employees table in ascending order of ID
    # select * from employees; 
    stmt = db.select(Employee).order_by(Employee.id.asc())
    employees = db.session.scalars(stmt)
    # Returning all instances in employees table with EmployeeSchema format
    return EmployeeSchema(many=True, exclude=['password']).dump(employees)

# fetch an instance from employees table that you want to retrieve
@employee_bp.route('/<int:id>/')
def employee_get_one(id):
    # Get an instance from employees table matching with parameter id
    # select * from employees where id = id
    stmt = db.select(Employee).filter_by(id=id)
    employee = db.session.scalar(stmt)
    if employee: # if found
        # Returning an instance in employees table with EmployeeSchema format except password
        return EmployeeSchema(exclude=['password']).dump(employee)
    else:
        # Returning not found error 404
        return {'error': f'Employee not found with id {id}'}, 404
    
# Create a new employee
@employee_bp.route('/', methods=['POST'])
# check if HR staff
@jwt_required()
def employee_create_one():
    # Using try: except: check if a new employees added is already in departments table 
    try:
        # change request.json to a format of python object
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
        # Return successful result with format of EmployeeSchema except password
        return EmployeeSchema(exclude=['password']).dump(employee), 201
    except IntegrityError:
        # Returning 409 error
        return {'error': 'Email address already exists'}, 409

# Update information of the employees table you chose     
@employee_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
# check if HR staff
@jwt_required()
def employee_update_one(id):
    # check if admin
    authorize()
    # get an instance of employees table matching with parameter ID 
    # select * from employees where id = id
    stmt = db.select(Employee).filter_by(id=id)
    employee = db.session.scalar(stmt)
    if employee: #if found
        # change request.json to a format of python object
        data = EmployeeSchema().load(request.json)
                
        employee.email = data.get('email') or employee.email
        employee.name = data.get('name') or employee.name
        employee.hire_date = data.get('hire_date') or employee.hire_date
        employee.salary = data.get('salary') or employee.salary
        employee.job_id = data.get('job_id') or employee.job_id
        employee.department_id = data.get('department_id') or employee.department_id
        db.session.commit()
        # Return successful result for update with format of EmployeeSchema
        return EmployeeSchema(exclude=['password']).dump(employee)
    else:
        return {'error' : f'Employee not found with id {id}'}, 404

# Delete one instance in employees table that you want to delete  
@employee_bp.route('/<int:id>', methods=['DELETE'])
# check if HR staff
@jwt_required()
def employee_delete_one(id):
    # check if admin
    authorize()
    # get an instance of employees table matching with parameter ID 
    # select * from employees where id = id
    stmt = db.select(Employee).filter_by(id=id)
    employee = db.session.scalar(stmt)
    if employee: # if found
        db.session.delete(employee)
        db.session.commit()
        # Returning successful message when deleted
        return {'message' : f'Employee id {id} deleted successfully'}
    else:
        # Returning not found error 404
        return {'error' : f'Employee not found with id {id}'}, 404
