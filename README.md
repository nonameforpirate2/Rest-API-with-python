# Rest-API-with-python
This repo has code to create  a rest api with python
# Create an API Service
Requierements:
    - One service for all tables.
    - A relational DB.
    - Data rule 1: log information in db when the data cannot be uploaded.
    - Data rule 2: all the fields are requiere.
    - Insert batch transactions up to 1000 items.
    - Create feature to backup.
## Create an API Service: DB Setup
In this section you can find how do I accomplish the database setup. I choose postgres db as my relational database for the api service.   
Achivements:   
    - Data rule 2: got implemented by means of setting up in the `setup_db.sql`(db_setup folder) script as not null certain columns during the parametrization and creation process of the tables.    
    - The relational db got implemented. In this case I use postgres.   
The information got insert into the DB with the help of the `insert_info.sql` script (db_setup folder). In the image below you can appreciate the database working on my laptop.   
Here is the database working:   
![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_1/database_setup_working.png "Database working")  
Here is the tables working:  
![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_1/database_tables_working.png "Tables working")
## Create an API Service: API working
In the script `rest_api.py` ("part 1" folder) you can find the script that I use to interact with the database as an API. In the picture below you can appreciate the script working.   
![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_1/running_script_working.png "API Script Working")
The `rest_conf.yml` file was use to substract sensitive information to interact to the database. We do not want a script with passowords or user names going public in the wrong place.    
In the image below you can appreciate the new data insertion into the departments table working with the API running local on postman.
![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_1/departments_insertion_working.png "API Departments Insertion Working")
