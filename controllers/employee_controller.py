from datetime import timedelta
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
    

      
