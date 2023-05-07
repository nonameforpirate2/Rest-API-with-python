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

        def __init__(self, department_name):
            self.department_name = department_name
  
    class DepartmentSchema(ma.Schema):
        class Meta:
            fields = ('department_id', 'department_name')

    department_schema = DepartmentSchema() 
    departments_schema = DepartmentSchema(many=True)

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
            department_name = request.json['department_name']
            department = Departments(department_name)
            db.session.add(department)
            db.session.commit()

            return jsonify({
                'Message': f'Department {department_name} inserted.'
            })

        @staticmethod
        def put():
            try: department_id = request.args['department_id']
            except Exception as _: department_id = None

            if not department_id:
                return jsonify({ 'Message': 'Must provide the user ID' })

            department = Departments.query.get(department_id)
            department_name = request.json['department_name']
           
            department.department_name = department_name
            
            db.session.commit()
            return jsonify({
                'Message': f'Department {department_name} altered.'
            })
        
        @staticmethod
        def delete():
            try: department_id = request.args['department_id']
            except Exception as _: department_id = None

            if not department_id:
                return jsonify({ 'Message': 'Must provide the user ID' })

            department = Departments.query.get(department_id)
            db.session.delete(department)
            db.session.commit()

            return jsonify({
                'Message': f'Department {str(department_id)} deleted.'
            })
        
    api.add_resource(DepartmentManager, '/api/departments')

    app.run(debug=True)