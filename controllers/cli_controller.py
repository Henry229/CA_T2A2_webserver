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
    employees = [
        Employee(
          email = 'admin@spam.com',
          name = 'Tom Cruise',
          password = bcrypt.generate_password_hash('1234').decode('utf-8'),
          hire_date = date.today(),
          salary = 150000
        ),
        Employee(
          email = 'first@spam.com',
          name = 'John Doe',
          password = bcrypt.generate_password_hash('1234').decode('utf-8'),
          hire_date = date.today(),
          salary = 60000
        ),
        Employee(
          email = 'second@spam.com',
          name = 'Henry Green',
          password = bcrypt.generate_password_hash('1234').decode('utf-8'),
          hire_date = date.today(),
          salary = 100000
        ),
        Employee(
          email = 'third@spam.com',
          name = 'Brad Fitts',
          password = bcrypt.generate_password_hash('1234').decode('utf-8'),
          hire_date = date.today(),
          salary = 200000
        ),
        Employee(
          email = 'fourth@spam.com',
          name = 'Mel Gibson',
          password = bcrypt.generate_password_hash('1234').decode('utf-8'),
          hire_date = date.today(),
          salary = 250000
        ),
        Employee(
          email = 'fifth@spam.com',
          name = 'Amandar Foster',
          password = bcrypt.generate_password_hash('1234').decode('utf-8'),
          hire_date = date.today(),
          salary = 90000
        )
    ]
    
    db.session.add_all(employees)
    db.session.commit()
    
    departments = [
        Department(
            department_name = 'IT development',
        ),
        Department(
            department_name = 'Houman Resources',
        ),
        Department(
            department_name = 'Sales',
        ),
        Department(
            department_name = 'Supports',
        ),
    ]
    
    db.session.add_all(departments)
    db.session.commit()
    
    jobs = [
        Job(
          job_title = 'Junior',
        ),
        Job(
          job_title = 'Senior',
        ),
        Job(
          job_title = 'Lead',
        ),
        Job(
          job_title = 'Manager',
        ),
        Job(
          job_title = 'Director',
        ),
        Job(
          job_title = 'CEO',
        ),
    ]
    
    db.session.add_all(jobs)
    db.session.commit()
    
    print('Talbes seeded!!!')