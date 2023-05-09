from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
import yaml
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import datetime
import logging

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
        password=password,
        host=hostname,
        database=db_name
    )

    app = Flask(__name__) 
    api = Api(app) 
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    db = SQLAlchemy(app) 
    ma = Marshmallow(app)

    class Departments(db.Model):
        department_id = db.Column(db.Integer, primary_key=True)
        department_name = db.Column(db.String(32), unique=True)

        def __init__(self, department_id, department_name):
            self.department_id = department_id
            self.department_name = department_name

    class Jobs(db.Model):
        job_id = db.Column(db.Integer, primary_key=True)
        job_name = db.Column(db.String(200), unique=True)

        def __init__(self, job_id, job_name):
            self.job_id = job_id
            self.job_name = job_name

    class Employees(db.Model):
        employee_id = db.Column(db.Integer, primary_key=True)
        employee_name = db.Column(db.String(200), unique=True)
        hire_date = db.Column(db.Date)
        department_id = db.Column(db.Integer)
        job_id = db.Column(db.Integer)

        def __init__(self, employee_id, employee_name, hire_date, department_id, job_id):
            self.employee_id = employee_id
            self.employee_name = employee_name
            self.hire_date = hire_date
            self.department_id = department_id
            self.job_id = job_id
  
    class DepartmentSchema(ma.Schema):
        class Meta:
            fields = ('department_id', 'department_name')

    class JobSchema(ma.Schema):
        class Meta:
            fields = ('job_id', 'job_name')

    class EmployeeSchema(ma.Schema):
        class Meta:
            fields = ('employee_id', 'employee_name', 'hire_date', 'department_id', 'job_id')


    department_schema = DepartmentSchema() 
    departments_schema = DepartmentSchema(many=True)

    job_schema = JobSchema() 
    jobs_schema = JobSchema(many=True)

    employee_schema = EmployeeSchema()
    employees_schema = EmployeeSchema(many=True)
        
    class DepartmentManager(Resource): 

        @staticmethod
        def get():
            try: department_id = request.args['department_id']
            except Exception as _: department_id = None

            if not department_id:
                departments = Departments.query.all()
                return jsonify(departments_schema.dump(departments))
            department = Departments.query.get(department_id)
            return jsonify(department_schema.dump(department))

        @staticmethod
        def post():
            n = 0
            departments_list_to_load = []
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

            logger = logging.getLogger('my_application')
            logger.setLevel(logging.ERROR)

            fh = logging.FileHandler("logs.log")
            fh.setLevel(logging.ERROR)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter) 

            logger.addHandler(fh)
            for item in request.get_json():
                n = n + 1
                if n <= 1000:
                    try:
                        department_id = item['department_id']
                        department_name = item['department_name']
                        department = Departments(department_id = department_id,
                                                department_name=department_name)
                        departments_list_to_load.append(department)
                    except Exception as e: 
                        logger.exception(e)
                else:
                    print("no more than 5 items!")

            db.session.add_all(departments_list_to_load)
            db.session.commit()

            return jsonify({
                'Message': f'{str(len(departments_list_to_load))} departments were inserted.'
            })
        
        
        @staticmethod
        def delete():
            try: department_id = request.args['department_id']
            except Exception as _: department_id = None

            if not department_id:
                return jsonify({ 'Message': 'Must provide the department ID' })
            
            items_to_delete = []
            for item in request.get_json():
                department = Departments.query.get(item["department_id"])
                items_to_delete.append(item["department_id"])
                print("erasing " + str(item["department_id"]))
                db.session.delete(department)
                db.session.commit()
                
            return jsonify({
                'Message': f'Department {str(len(items_to_delete))} deleted.'
            })
        
    class JobManager(Resource): 

        @staticmethod
        def get():
            try: job_id = request.args['job_id']
            except Exception as _: job_id = None

            if not job_id:
                jobs = Jobs.query.all()
                return jsonify(jobs_schema.dump(jobs))
            job = Jobs.query.get(job_id)
            return jsonify(job_schema.dump(job))

        @staticmethod
        def post():
            n = 0
            jobs_list_to_load = []
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

            logger = logging.getLogger('my_application')
            logger.setLevel(logging.ERROR)

            fh = logging.FileHandler("logs.log")
            fh.setLevel(logging.ERROR)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter) 

            logger.addHandler(fh)
            for item in request.get_json():
                n = n + 1
                if n <= 1000:
                    try:
                        job_id = item['job_id']
                        job_name = item['job_name']
                        job = Jobs(job_id = job_id,
                                    job_name=job_name)
                        jobs_list_to_load.append(job)
                    except Exception as e: 
                        logger.exception(e)
                else:
                    print("no more than 5 items!")

            db.session.add_all(jobs_list_to_load)
            db.session.commit()

            return jsonify({
                'Message': f'{str(len(jobs_list_to_load))} jobs were inserted.'
            })
        
        
        @staticmethod
        def delete():
            try: job_id = request.args['job_id']
            except Exception as _: job_id = None

            if not job_id:
                return jsonify({ 'Message': 'Must provide the job ID' })
            
            items_to_delete = []
            for item in request.get_json():
                job = Jobs.query.get(item["job_id"])
                items_to_delete.append(item["job_id"])
                print("erasing " + str(item["job_id"]))
                db.session.delete(job)
                db.session.commit()
                
            return jsonify({
                'Message': f'Jobs {str(len(items_to_delete))} deleted.'
            })
        
    class EmployeeManager(Resource): 

        @staticmethod
        def get():
            try: employee_id = request.args['employee_id']
            except Exception as _: employee_id = None

            if not employee_id:
                employees = Employees.query.all()
                return jsonify(employees_schema.dump(employees))
            employee = Employees.query.get(employee_id)
            return jsonify(job_schema.dump(employee))

        @staticmethod
        def post():
            n = 0
            employees_list_to_load = []
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

            logger = logging.getLogger('my_application')
            logger.setLevel(logging.ERROR)

            fh = logging.FileHandler("logs.log")
            fh.setLevel(logging.ERROR)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter) 

            logger.addHandler(fh)
            for item in request.get_json():
                n = n + 1
                if n <= 1000:
                    try:
                        print("here is the item@!!!!!!!!")
                        print(item)
                        employee_id = item['employee_id']
                        employee_name = item['employee_name']
                        hire_date = item['hire_date']
                        department_id = item['department_id']
                        job_id = item['job_id']
                        employee = Employees(employee_id = employee_id,
                                    employee_name = employee_name,
                                    hire_date = hire_date,
                                    department_id = department_id,
                                    job_id = job_id)
                        employees_list_to_load.append(employee)
                    except Exception as e: 
                        logger.exception(e)
                else:
                    print("no more than 5 items!")

            db.session.add_all(employees_list_to_load)
            db.session.commit()

            return jsonify({
                'Message': f'{str(len(employees_list_to_load))} employees were inserted.'
            })
        
        
        @staticmethod
        def delete():
            try: employee_id = request.args['employee_id']
            except Exception as _: employee_id = None

            if not employee_id:
                return jsonify({ 'Message': 'Must provide the job ID' })
            
            items_to_delete = []
            for item in request.get_json():
                employee = Employees.query.get(item["employee_id"])
                items_to_delete.append(item["employee_id"])
                print("erasing " + str(item["employee_id"]))
                db.session.delete(employee)
                db.session.commit()
                
            return jsonify({
                'Message': f'Employees {str(len(items_to_delete))} deleted.'
            })
        
    api.add_resource(DepartmentManager, '/api/departments')
    api.add_resource(JobManager, '/api/jobs')
    api.add_resource(EmployeeManager, '/api/employees')

    app.run(debug=True)