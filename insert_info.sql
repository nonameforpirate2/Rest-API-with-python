/* Here I am inserting data on departments table.*/
COPY DEPARTMENTS(DEPARTMENT_ID, DEPARTMENT_NAME)
FROM 'C:\Users\g1238\Documents\GitHub\Rest-API-with-python\data_csv\departments.csv'
DELIMITER ','
CSV HEADER;

/* Here I am inserting data on jobs table.*/
COPY JOBS(JOB_ID, JOB_NAME)
FROM 'C:\Users\g1238\Documents\GitHub\Rest-API-with-python\data_csv\jobs.csv'
DELIMITER ','
CSV HEADER;

/* Here I am inserting data on employees table.*/
COPY EMPLOYEES(EMPLOYEE_ID,EMPLOYEE_NAME,HIRE_DATE,DEPARTMENT_ID,JOB_ID)
FROM 'C:\Users\g1238\Documents\GitHub\Rest-API-with-python\data_csv\hired_employees.csv'
DELIMITER ','
CSV HEADER;