from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
import yaml
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


if __name__ == '__main__':
    
    with open('rest_conf.yml', 'r') as file:
            config = yaml.safe_load(file)

    #Authenticator Credentials
    user = config['rest_api']['user_name'][0]
    password = config['rest_api']['password'][0]
    hostname = config['rest_api']['host'][0]
    db_name = config['rest_api']['database'][0]
    db_url = config['rest_api']['database_url'][0]
    driver_name = config['rest_api']['driver_name'][0]

    url = URL.create(
        drivername=driver_name,
        username=user,
        host=hostname,
        database=db_name
    )

    rest_app = Flask(__name__) 
    api = Api(rest_app) 
    rest_app.config['SQLALCHEMY_DATABASE_URI'] = url
    rest_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    db = SQLAlchemy(rest_app) 
    ma = Marshmallow(rest_app)

    class Departments(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        department_name = db.Column(db.String(64), unique=True)

        def __init__(self, department_name):
            self.department_name = department_name

    class Jobs(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        job_name = db.Column(db.String(64), unique=True)

        def __init__(self, job_name):
            self.job_name = job_name

    class Employees(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        employee_name = db.Column(db.String(32), unique=True)
        hire_date = db.Column(db.Date)
        department_id = db.Column(db.Integer)
        job_id = db.Column(db.Integer)

        def __init__(self, employee_name, hire_date, department_id, job_id):
            self.employee_name = employee_name
            self.hire_date = hire_date
            self.department_id = department_id
            self.job_id = job_id

    class DepartmentsSchema(ma.Schema):
        class Meta_Departments:
            fields = ('id', 'department_name')

    class JobSchema(ma.Schema):
        class Meta_Jobs:
            fields = ('id', 'job_name')

    class EmployeeSchema(ma.Schema):
        class Meta_Employees:
            fields = ('id', 'employee_name', 'hire_date', 'department_id', 'job_id')

    employee_schema = EmployeeSchema() 
    employees_schema = EmployeeSchema(many=True)

    class Resource_Manager(Resource): 

        @staticmethod
        def get():
            try: id = request.args['id']
            except Exception as _: id = None
            if not id:
                employees = Employees.query.all()
                return jsonify(employees_schema.dump(employees))
            employee = Employees.query.get(id)
            return jsonify(employee_schema.dump(employee))
            pass

        @staticmethod
        def post():
            employee_name = request.json['employee_name']
            hire_date = request.json['hire_date']
            department_id = request.json['department_id']
            job_id = request.json['job_id']

            employee = Employees(employee_name, hire_date, department_id, job_id)
            db.session.add(user)
            db.session.commit()

            return jsonify({
                'Message': f'User {employee_name} {hire_date} inserted.'
            })

    rest_app.run(debug=True)

    api.add_resource(Resource_Manager, '/api/employees')