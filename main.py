from flask import Flask
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.auth_controller import auth_bp
from controllers.employee_controller import employee_bp
from controllers.department_controller import department_bp
from controllers.job_controller import job_bp
from marshmallow.exceptions import ValidationError
import os

def create_app():
    app = Flask(__name__)
    
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': err.messages}, 400
    
    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 440
    
    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': str(err)}, 401
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(department_bp)
    app.register_blueprint(job_bp)
    
    return app  
    