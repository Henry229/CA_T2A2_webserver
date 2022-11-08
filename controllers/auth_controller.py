from datetime import timedelta
# from xml.etree.ElementInclude import include
from flask import Blueprint, request, abort, json
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import join
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from init import db, bcrypt
from models.employee import Employee, EmployeeSchema
from models.hrstaff import Hrstaff, HrstaffSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/')
def auth_get_hrstaff():
    stmt = db.select(Hrstaff).order_by(Hrstaff.id.asc())
    hrstaffs = db.session.scalars(stmt)
    return HrstaffSchema(many=True).dump(hrstaffs)
  
@auth_bp.route('/login', methods=['POST'])
def auth_login():
    stmt = db.select(Employee).join(Employee.hrstaffs).filter(Employee.email == request.json['email'])
    employee = db.session.scalar(stmt)
    
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
    stmm = db.select(Hrstaff).filter_by(employee_id = employee.id)
    staff = db.session.scalar(stmm)
    if not staff:
        if employee and employee.department_id == 1:
            data = HrstaffSchema().load(request.json)
            hrstaff = Hrstaff(
                        employee_id = employee.id,
                        is_admin = data.get('is_admin')
                        )
            db.session.add(hrstaff)
            db.session.commit()
            
            return HrstaffSchema().dump(hrstaff), 201
        else:
            return {'message': f'{employee.email} is not HR staff'}, 404
    else:
        return {'error' : f'{employee.email} is already in HRstaff table'}, 409
    
@auth_bp.route('/update/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def auth_update(id):
    authorize()
    stmm = db.select(Hrstaff).filter_by(id = id)
    staff = db.session.scalar(stmm)
    data = HrstaffSchema().load(request.json)
    if staff:
        if not request.json.get('employee_id') == None:
            stmt = db.select(Employee).filter_by(id = request.json.get('employee_id'))
            employee = db.session.scalar(stmt)
            if employee and employee.department_id == 1:
                staff.employee_id = data.get('employee_id')
                staff.is_admin = staff.is_admin
            elif not employee:
                return {'error' : f'{employee.id} is not found'}, 404
            elif employee.department_id != 1:
                return {'message': f'{employee.id} is not HR staff'}
        if not request.json.get('is_admin') == None:
            staff.employee_id = staff.employee_id
            staff.is_admin = data.get('is_admin')
        db.session.commit()
        return HrstaffSchema().dump(staff), 201
    else:
        return {'error': f'staff id {id} is not HR staff'}
  
@auth_bp.route('/delete/<int:id>/', methods=['DELETE'])
@jwt_required()
def auth_delete_one(id):
    authorize()
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