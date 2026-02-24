CREATE DATABASE IF NOT EXISTS test_db;
USE test_db;

CREATE TABLE IF NOT EXISTS employees (
    emp_no INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(55) NOT NULL,
    last_name VARCHAR(55) NOT NULL,
    hire_date DATE
);

CREATE TABLE IF NOT EXISTS salaries (
    emp_no INT,
    salary INT,
    from_date DATE,
    to_date DATE,
    FOREIGN KEY (emp_no) REFERENCES employees(emp_no)
);

INSERT INTO employees VALUES (1, 'Ahmed', 'Medhat', '2026-01-01'), (2, 'Marwan', 'Essa', '2026-01-01');
INSERT INTO salaries VALUES (1, 10000, '2026-01-01', '2026-12-01'), (2, 10000, '2026-01-01', '2026-12-01');