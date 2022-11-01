from datetime import timedelta
from flask import Blueprint, request, abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from init import db, bcrypt
from models.employee import Employee, EmployeeSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/employees/')
def auth_get_employees():
    stmt = db.select(Employee).order_by(Employee.id.asc())
    employees = db.session.scalars(stmt)
    return EmployeeSchema(many=True, exclude=['password']).dump(employees)
  
@auth_bp.route('/login', methods=['POST'])
def auth_login():
    stmt = db.select(Employee).filter_by(email = request.json['email'])
    employee = db.session.scalar(stmt)
    
    if employee and bcrypt.check_password_hash(employee.password, request.json['password']):
        access_token = create_access_token(identity=str(employee.id), expires_delta=timedelta(days=1))
        return {'email': employee.email, 'name': employee.name, 'access_token': access_token}
      
@auth_bp.route('/logout/', methods=['DELETE'])
@jwt_required()
def auth_logout():
    return {'massage': f'{get_jwt_identity()} is logout '}