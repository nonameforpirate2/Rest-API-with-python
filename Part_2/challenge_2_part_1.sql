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

DROP TABLE IF EXISTS employees_per_quarter_t1;
CREATE TEMPORARY TABLE employees_per_quarter_t1 AS(
SELECT
	department_name as department,
	job_name as job,
	CASE
		when quarter = 1 then 'Q1'
		when quarter = 2 then 'Q2'
		when quarter = 3 then 'Q3'
		else 'Q4'
	END AS quarter_name,
	1 as cnt_employees
FROM employees_clean
WHERE years = 2021
	AND job_id != 0
	AND department_id != 0
);

DROP TABLE IF EXISTS employees_per_quarter_t2;
CREATE TEMPORARY TABLE employees_per_quarter_t2 AS (
SELECT
	department,
	job,
	quarter_name,
	SUM(cnt_employees) AS cnt
FROM employees_per_quarter_t1
GROUP BY department,
	job,
	quarter_name
);

DROP TABLE IF EXISTS employees_per_quarter_t3;
CREATE TEMPORARY TABLE employees_per_quarter_t3 AS (
SELECT 
	department,
	job,
	MAX(case when (quarter_name='Q1') then cnt else 0 end) as Q1,
	MAX(case when (quarter_name='Q2') then cnt else 0 end) as Q2,
	MAX(case when (quarter_name='Q3') then cnt else 0 end) as Q3,
	MAX(case when (quarter_name='Q4') then cnt else 0 end) as Q4
FROM employees_per_quarter_t2
group by department, job
order by department, job
);

DROP TABLE IF EXISTS challenge_2_part_1;
CREATE TABLE challenge_2_part_1 AS (
SELECT * 
FROM employees_per_quarter_t3
);