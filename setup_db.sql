/* Here is a nice description out of my script
   I am creating the database for the project in here :) .*/
DROP DATABASE IF EXISTS EMPLOYEES_INFO;
CREATE DATABASE EMPLOYEES_INFO;

/* This table has the schema to store tables. */
DROP SCHEMA IF EXISTS EMPLOYEES_INFO;
CREATE SCHEMA EMPLOYEES_INFO;

/* This table has the list of jobs available at the company. */
CREATE TABLE JOBS (
    JOB_ID SERIAL PRIMARY KEY,
    JOB_NAME VARCHAR(255) NOT NULL
);

/* This table has the list of departments available at the company. */
CREATE TABLE DEPARTMENTS (
    DEPARTMENT_ID SERIAL PRIMARY KEY,
    DEPARTMENT_NAME VARCHAR(255) NOT NULL
);

/* This table has the list of employees working at the company
   it cointains their id, name, date when they got hired, 
   department id and id from their jobs. */
CREATE TABLE EMPLOYEES(
    EMPLOYEE_ID SERIAL PRIMARY KEY,
    EMPLOYEE_NAME VARCHAR(255) NULL,
    HIRE_DATE TIMESTAMP NULL,
    DEPARTMENT_ID INTEGER NULL,
    JOB_ID INTEGER NULL
);