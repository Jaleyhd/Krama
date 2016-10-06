DROP TABLE executions_tab;
CREATE TABLE executions_tab
(
exec_id INT NOT NULL,
project_name VARCHAR(512),
project_path VARCHAR(2048),
job_name VARCHAR(512),
depends_on VARCHAR(2048),
status INT NOT NULL,
pid INT DEFAULT -1,
start_time BIGINT DEFAULT -1,
end_time  BIGINT DEFAULT -1, 
retry INT,
completion_percentage FLOAT DEFAULT -1.0,
PRIMARY KEY(exec_id,project_name,job_name)
);