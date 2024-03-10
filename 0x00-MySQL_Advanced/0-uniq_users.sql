-- create table users
-- id is unique and primary key
CREATE TABLE IF NOT EXISTS users
       (id INT PRIMARY KEY UNIQUE NOT NULL AUTO_INCREMENT,
       email VARCHAR(255) UNIQUE NOT NULL,
       name VARCHAR(255)
       );
