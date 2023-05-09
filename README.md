# Rest-API-with-python
This repo has code to create  a rest api with python
# Create an API Service (Challenge Part 1)
Requierements:
    - One service for all tables.
    - A relational DB.
    - Data rule 1: log information in db when the data cannot be uploaded.
    - Data rule 2: all the fields are requiere.
    - Insert batch transactions up to 1000 items.
    - Create feature to backup.
### Create an API Service: DB Setup
In this section you can find how do I accomplish the database setup. I choose postgres db as my relational database for the api service.   
Achivements:   
    - Data rule 2: got implemented by means of setting up in the `setup_db.sql`(db_setup folder) script as not null certain columns during the parametrization and creation process of the tables.    
    - The relational db got implemented. In this case I use postgres.   
The information got insert into the DB with the help of the `insert_info.sql` script (db_setup folder). In the image below you can appreciate the database working on my laptop.   
Here is the database working:   
![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_1/database_setup_working.png "Database working")  
Here is the tables working:  
![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_1/database_tables_working.png "Tables working")
### Create an API Service: API working
In the script `rest_api.py` ("part 1" folder) you can find the script that I use to interact with the database as an API. In the picture below you can appreciate the script working.   
![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_1/running_script_working.png "API Script Working")
The `rest_conf.yml` file was use to substract sensitive information to interact to the database. We do not want a script with passowords or user names going public in the wrong place.    
In the image below you can appreciate the new data insertion into the departments table working with the API running local on postman.
![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_1/departments_insertion_working.png "API Departments Insertion Working")
In the image below you can appreciate the new data insertion into the jobs table working with the API running local on postman.  
![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_1/jobs_insertion_working.png "API Jobs Insertion Working")
In the image below you can appreciate the new data insertion into the employees table working with the API running local on postman.   
![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_1/employees_insertion_working.png "API Employees Insertion Working")
Achievements:  
    - Transactions that don't accomplish the rules must not be inserted but they must be logged. I manage to accomplish the requirement by means of adding logs tracking in case of error, configuring the tables to only accept its corresponding datatype and rejecting empty registers. By default the db will reject json objects with empty spaces or wrong datatype. You can appreciate in the image below a log generated log file out of an attemp to insert a record with an id which already existed.
    ![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_1/logs_working_part_1.png "Log File creation working properly")  
    In the image below is the code where I programmed the log file generation while attemping to insert data into the db.
    ![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_1/logs_working_part_2.png "Log file code to track errors working.")  

### Create an API Service: Feature to back up the information
Unfortunately postgres does not have commands to save tables into avro format. As you can see in the image below, in the postgres documentation.  
![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_1/postgres_only_has_tar_files_backups.png "Postgres Just Backs up Data on TAR or GZIP")  
For this reason I have to back up the data on tar format. Furthermore, the only way that you can do it is by means of scheduling in linux to run the command from psql with x frequency. In this case I schedule to do a back up on Saturdays at midgnight. Here is the image to schedule the backup.
![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_1/backup_schedule_saturdays_midnight_on_linux.png "Backups from Postgres working automatically on Linux.") 

# Aggregate Data to Generate Reports (Challenge Part 2)
In this case scenario. I needed to aggregate the corresponding information to generate the specify outcome. In the image below you can appreciate the data architecture for the solution.
![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_2/data_architecture_challenge_2.png "Data Architecture for the Solution.") 
I choose to add as scheduling jobs in the Postgres DB two scripts which generate the outcome for part 1 challenge 2 and part 2 challenge 2. In the script `challenge_2_part_1.sql` (part_2 folder) you can find the aggregation done to generate outcome for part 1. The script was added into a scheduling job to run with a certain frequency to drop and generate again the table. Thus, Tableau visualizations will be always updated automatically since it connects directly to the output table.   
In the script `challenge_2_part_2.sql` (part_2 folder) you can find the aggregations done to generate outcome for part 2. The script was added into a scheduling job in Postgres DB and Tableau connects to the outcome table 2.   
In the image below you can appreciate the scheduled jobs in Postgres DB.   
![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_2/scheduling_jobs_part_2.png "Scheduled jobs in Postgres DB.") 
## Aggregate Data to Generate Reports: Visualization
As a matter of extra. I include a couple of tableau visualizations into the solution. The visualizations are the product out of the analysis. In the file `challenge_2_part_1.twbx` (part_2 folder) you can find the tableau compress file including the data to open it and manipulate the visualizations. In the image below you an appreciate the total hiring positions per department. It corresponds to the part 1.  
![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_2/total_hiring_positions.png "Total Hiring Positions Per Department.")    
In the image below you can appreciate the hiring flow over the last year per department on quarterly basis. It corresponds to the part 1.   
![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_2/hiring_flow_last_year.png "Hiring Flow.")    
The image below represents the positions distributions per deparment and you can appreciate proportions by team during q4.
![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_2/Positions_distributions_over_departments_q4.png "Position Distributions over Departments Q4.")     
In the file `challenge_2_part_2.twbx` (part_2 folder) you can find the tableau compress file including the data to check visualizations.  
In the image below you can see a visualization for the output table given desire aggregations. It corresponds to the part 2 of the challenge.  
![alt text](https://github.com/nonameforpirate2/Rest-API-with-python/blob/dev/Part_2/Top_Hiring_Departments_Over_The_Mean.png "Top Hiring Departments Over the Mean.")  


