from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.hrstaff import Hrstaff
from models.employee import Employee
from models.department import Department
from models.job import Job

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print('Tables create successfully!!')

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Tables drop successfully!!')
    
 
@db_commands.cli.command('seed')
def seed_db():
    departments = [
        Department(
            department_name = 'Human Resources',
        ),
        Department(
            department_name = 'IT development',
        ),
        Department(
            department_name = 'Sales',
        ),
    ]
    
    db.session.add_all(departments)
    db.session.commit()
       
    jobs = [
        Job(
          job_position = 'Junior',
        ),
        Job(
          job_position = 'Senior',
        ),
        Job(
          job_position = 'Lead',
        ),
        Job(
          job_position = 'Manager',
        ),
        Job(
          job_position = 'Director',
        ),
        Job(
          job_position = 'CEO',
        ),
    ]
    
    db.session.add_all(jobs)
    db.session.commit()


    employees = [
        Employee(
          email = 'admin@spam.com',
          name = 'Tom Cruise',
          password = bcrypt.generate_password_hash('1234').decode('utf-8'),
          hire_date = date.today(),
          salary = 150000,
          job = jobs[3],
          department = departments[0]
        ),
        Employee(
          email = 'first@spam.com',
          name = 'John Doe',
          password = bcrypt.generate_password_hash('1234').decode('utf-8'),
          hire_date = date.today(),
          salary = 150000,
          job = jobs[3],
          department = departments[1]
        ),
        Employee(
          email = 'second@spam.com',
          name = 'Henry Green',
          password = bcrypt.generate_password_hash('1234').decode('utf-8'),
          hire_date = date.today(),
          salary = 150000,
          job = jobs[3],
          department = departments[2]
        ),
        Employee(
          email = 'third@spam.com',
          name = 'Brad Fitts',
          password = bcrypt.generate_password_hash('1234').decode('utf-8'),
          hire_date = date.today(),
          salary = 200000,
          job = jobs[4],
          department = departments[2]
        ),
        Employee(
          email = 'fourth@spam.com',
          name = 'Mel Gibson',
          password = bcrypt.generate_password_hash('1234').decode('utf-8'),
          hire_date = date.today(),
          salary = 300000,
          job = jobs[5],
          department = departments[0]
        ),
        Employee(
          email = 'fifth@spam.com',
          name = 'Amanda Foster',
          password = bcrypt.generate_password_hash('1234').decode('utf-8'),
          hire_date = date.today(),
          salary = 80000,
          job = jobs[0],
          department = departments[1]
        ),
        Employee(
          email = 'sixth@spam.com',
          name = 'Sam Strong',
          password = bcrypt.generate_password_hash('1234').decode('utf-8'),
          hire_date = date.today(),
          salary = 80000,
          job = jobs[0],
          department = departments[0]
        ),
        Employee(
          email = 'seventh@spam.com',
          name = 'Austin Heizle',
          password = bcrypt.generate_password_hash('1234').decode('utf-8'),
          hire_date = date.today(),
          salary = 100000,
          job = jobs[1],
          department = departments[2]
        ),
        Employee(
          email = 'eighth@spam.com',
          name = 'Alex Google',
          password = bcrypt.generate_password_hash('1234').decode('utf-8'),
          hire_date = date.today(),
          salary = 100000,
          job = jobs[1],
          department = departments[1]
        ),
    ]
    
    db.session.add_all(employees)
    db.session.commit()
    
    hrstaffs = [
        Hrstaff(
            employees = employees[0],
            is_admin = True
        ),
        Hrstaff(
            employees = employees[4],
            is_admin = False
        ),
        
    ]
    
    db.session.add_all(hrstaffs)
    db.session.commit()
       
    
    print('Talbes seeded!!!')