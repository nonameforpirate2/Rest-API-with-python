/*Fix empty values with 0*/
DROP TABLE IF EXISTS employees_clean;
CREATE TEMPORARY TABLE employees_clean AS (
select 
	employee_id,
	employee_name,
	EXTRACT(YEAR FROM hire_date) as years,
	EXTRACT(QUARTER FROM hire_date) as quarter,
	COALESCE(employees.department_id,0) as department_id,
	COALESCE(employees.job_id,0) as job_id,
	departments.department_name,
	jobs.job_name
from employees
LEFT JOIN departments
	on departments.department_id = employees.department_id
LEFT JOIN jobs
	on employees.job_id = jobs.job_id
);

DROP TABLE IF EXISTS employees_per_department_t1;
CREATE TEMPORARY TABLE employees_per_department_t1 AS(
SELECT
	department_id,
	department_name,
	1 as cnt_employees
FROM employees_clean
WHERE years = 2021
	AND job_id != 0
	AND department_id != 0
);
/* CHECK MEAN EMPLOYEES HIRE PER DEPARTMENT ON 2021*/
DROP TABLE IF EXISTS TOTAL_EMPLOYEES_PER_DEPARTMENT_2021;
CREATE TEMPORARY TABLE TOTAL_EMPLOYEES_PER_DEPARTMENT_2021 AS (
SELECT
	department_id,
	department_name,
	SUM(cnt_employees) as cnt_employees_hire
FROM employees_per_department_t1
	group by department_id, department_name
);

DROP TABLE IF EXISTS MEAN_EMPLOYEES_PER_DEPARTMENT_2021;
CREATE TEMPORARY TABLE MEAN_EMPLOYEES_PER_DEPARTMENT_2021 AS (
SELECT AVG(cnt_employees_hire) FROM TOTAL_EMPLOYEES_PER_DEPARTMENT_2021
);

/*Given aggregations from above in average each department hire 138.25 (I will round it to 138) people on 2021.*/

DROP TABLE IF EXISTS challenge_2_part_2;
CREATE TABLE challenge_2_part_2 AS (
SELECT 
	department_id,
	department_name,
	cnt_employees_hire as hire
FROM TOTAL_EMPLOYEES_PER_DEPARTMENT_2021
WHERE cnt_employees_hire > 138
ORDER BY cnt_employees_hire DESC
);

SELECT * FROM challenge_2_part_2;


