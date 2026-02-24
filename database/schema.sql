CREATE DATABASE IF NOT EXISTS metrics_db;
USE metrics_db;

CREATE TABLE IF NOT EXISTS queries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sql_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS query_metrics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    query_id INT NOT NULL,
    execution_time_ms FLOAT,
    rows_examined INT,
    rows_returned INT,
    joins_count INT,
    index_used VARCHAR(255),
    complexity_score INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (query_id) REFERENCES queries(id) ON DELETE CASCADE
);