from datetime import timedelta
import email
from xml.etree.ElementInclude import include
from flask import Blueprint, request, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import join
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from init import db, bcrypt
from models.employee import Employee, EmployeeSchema
from models.hrstaff import Hrstaff, HrstaffSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/')
def auth_get_hrstaff():
    stmt = db.select(Hrstaff).order_by(Hrstaff.id.asc())
    # stmt = db.select(Employee, Hrstaff.is_admin).\
    #           join(Employee.hrstaffs)
    hrstaffs = db.session.scalars(stmt)
              # filter(Hrstaff.is_admin == True)
    # return EmployeeSchema(many=True, exclude=['password']).dump(hrstaffs)
    return HrstaffSchema(many=True).dump(hrstaffs)
  
@auth_bp.route('/login', methods=['POST'])
def auth_login():
    stmt = db.select(Employee).join(Employee.hrstaffs).filter(Employee.email == request.json['email'])
    employee = db.session.scalar(stmt)
    # stmt = db.select(Employee).filter_by(email = request.json['email'])
    
    if employee: 
        if bcrypt.check_password_hash(employee.password, request.json['password']):
            access_token = create_access_token(identity=str(employee.id), expires_delta=timedelta(days=1))
            return {'email': employee.email, 'name': employee.name, 'access_token': access_token}
        else:
            return {'message': 'Invalid password'}
    else:
        return {'message': 'Only HR staffs can access'}
      
@auth_bp.route('/add/', methods=['POST'])
@jwt_required()
def auth_add():
    stmt = db.select(Employee).filter_by(email = request.json['email'])
    employee = db.session.scalar(stmt)
    if employee and employee.department_id == 1:
        try:
            hrstaff = Hrstaff(
                      employee_id = employee.id,
                      is_admin = request.json['is_admin']
                      )
            db.session.add(hrstaff)
            db.session.commit()
            
            return HrstaffSchema().dump(hrstaff), 201
        except IntegrityError:
            return {'error': f'{employee.id} already registered'}, 409
    else:
        return {'message': f'{employee.email} is not HR staff'}
      
# @auth_bp.route('/logout/', methods=['DELETE'])
# @jwt_required()
# def auth_logout():
#     return {'massage': f'{get_jwt_identity()} is logout '}
  
@auth_bp.route('/delete/<int:id>/', methods=['DELETE'])
@jwt_required()
def auth_delete_one(id):
    print('####Yogida1')
    authorize()
    print('####Yogida2')
    stmt = db.select(Hrstaff).filter_by(id=id)
    hrstaff = db.session.scalar(stmt)
    if hrstaff:
        db.session.delete(hrstaff)
        db.session.commit()
        return {'message' : f'Staff id {id} deleted successfully'}
    else:
        return {'error' : f'hrstaff not found with id {id}'}
  
def authorize():
    staff_id = get_jwt_identity()
    stmt = db.select(Hrstaff).join(Employee.hrstaffs).filter(Employee.id == staff_id)
    staff = db.session.scalar(stmt)
    if not staff.is_admin:
        abort(401)