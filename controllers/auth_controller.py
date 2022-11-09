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

# fetch all staffs in HR department 
@auth_bp.route('/')
def auth_get_hrstaff():
    # All instances of of the hrstaffs table in ascending order of ID 
    stmt = db.select(Hrstaff).order_by(Hrstaff.id.asc()) # select * from Hrstaff order by id asc
    hrstaffs = db.session.scalars(stmt)
    return HrstaffSchema(many=True).dump(hrstaffs) # Returning all staffs in HR department

# only HR staffs can login to manage all employees  
@auth_bp.route('/login', methods=['POST']) 
def auth_login():
    # Join Employees and Hrstaffs table with email to verify if it is a HR staff
    # select a.* from employees a JOIN hrstaffs b on a.id = b.employee_id where a.email = request.json['email']
    # 1. The above query means, find the same employee as the email you entered in the employees table and then get employees.id
    # 2. Check if there is the employee.id equal to a employee_id in hrstaffs table.
    # 3. get all instances of employees if it exists.
    stmt = db.select(Employee).join(Employee.hrstaffs).filter(Employee.email == request.json['email'])
    employee = db.session.scalar(stmt)
    
    if employee: 
        if bcrypt.check_password_hash(employee.password, request.json['password']):
            access_token = create_access_token(identity=str(employee.id), expires_delta=timedelta(days=1))
            # return staff identification information when login is successful
            return {'email': employee.email, 'name': employee.name, 'access_token': access_token}
        else:
            return {'message': 'Invalid password'} # return error when mismatch between 2 passwords
    else:
        return {'message': 'Only HR staffs can access'} # no staff in Hrstaffs table through JOIN statement

# create new HR staff      
@auth_bp.route('/add/', methods=['POST'])
# check if HR staff 
@jwt_required()
def auth_add():
    # Get an instance of employees table if email in employees and the email you entered is same
    # select * from employees where email = request.json['email']
    stmt = db.select(Employee).filter_by(email = request.json['email'])
    employee = db.session.scalar(stmt)
    # Get all instance of hrstaffs table if you find the same employee_id in hrstaffs with employee.id in employees 
    # select * from Hrstaffs where employee.id = employee.id 
    stmm = db.select(Hrstaff).filter_by(employee_id = employee.id)
    staff = db.session.scalar(stmm)
    if not staff:
        if employee and employee.department_id == 1: # if it is found and works at HR department
            # change request.json to a format of python object
            data = HrstaffSchema().load(request.json)
            hrstaff = Hrstaff(
                        employee_id = employee.id,
                        is_admin = data.get('is_admin')
                        )
            db.session.add(hrstaff)
            db.session.commit()
            
            return HrstaffSchema().dump(hrstaff), 201 # return result of creation with Hrstaff Schema
        else:
            return {'message': f'{employee.email} is not HR staff'}, 404 # not found anything that meets the condition
    else:
        return {'error' : f'{employee.email} is already in HRstaff table'}, 409 # email you entered is not found in hrstaffs table.
    
# Update information of the HR staff you chose
@auth_bp.route('/update/<int:id>', methods=['PUT', 'PATCH'])
# check if HR staff 
@jwt_required()
def auth_update(id):
    # check if admin 
    authorize()
    # get an instance of hrstaffs if you find the same id in hrstaffs table that was given with parameter.
    # select * from hrstaffs where id = id 
    stmm = db.select(Hrstaff).filter_by(id = id)
    staff = db.session.scalar(stmm)
    # change request.json to a format of python object
    data = HrstaffSchema().load(request.json)
    if staff:
        if not request.json.get('employee_id') == None:
            # get a instance of employees table if you find the same id with entered employee_id
            # select * from employees where id = request.json.get('employee_id')
            stmt = db.select(Employee).filter_by(id = request.json.get('employee_id'))
            employee = db.session.scalar(stmt)
            if employee and employee.department_id == 1: # if it is found and works at HR department
                staff.employee_id = data.get('employee_id')
                staff.is_admin = staff.is_admin
            elif not employee: # if you not find 
                # this will return a not found 404 error 
                return {'error' : f'{employee.id} is not found'}, 404
            elif employee.department_id != 1: # if not HR staff
                # this will return a not found 404 error 
                return {'message': f'{employee.id} is not HR staff'}, 404
        if not request.json.get('is_admin') == None: # request is_admin to update
            staff.employee_id = staff.employee_id
            staff.is_admin = data.get('is_admin')
        db.session.commit()
        return HrstaffSchema().dump(staff), 201 # return result with format of HrstaffSchema
    else:
        return {'error': f'staff id {id} is not HR staff'}, 404 # return error if not found HR staff 
  
# delete HR staff in hrstaffs table
@auth_bp.route('/delete/<int:id>/', methods=['DELETE'])
# check if HR staff 
@jwt_required()
def auth_delete_one(id):
    # check if admin
    authorize()
    # get an instance of hrstaffs table if mach with id in parameter
    # select * from hrstaffs where id = id
    stmt = db.select(Hrstaff).filter_by(id=id)
    hrstaff = db.session.scalar(stmt)
    if hrstaff: # if found what you want to delete
        db.session.delete(hrstaff)
        db.session.commit()
        # return message that is successfully deleted
        return {'message' : f'Staff id {id} deleted successfully'}
    else:
        # return error if not found what you want to delete
        return {'error' : f'hrstaff not found with id {id}'},404
  
# check if admin  
def authorize():
    staff_id = get_jwt_identity() # id in token
    # Join Employees and Hrstaffs table with employee.id to verify if it is a HR staff
    # select b.* from employees a JOIN hrstaffs b on a.id = b.employee_id where a.id = get_jwt_identity()
    # 1. The above query means, find the same employee.id as the staff_id that saved in token and then get employees.id
    # 2. Check if there is the employee.id equal to a employee_id in hrstaffs table.
    # 3. get all instances of hrstaffs if it exists.
    stmt = db.select(Hrstaff).join(Employee.hrstaffs).filter(Employee.id == staff_id)
    staff = db.session.scalar(stmt)
    if not staff.is_admin:
        abort(401)