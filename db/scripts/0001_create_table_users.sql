drop table users;

CREATE TABLE IF NOT EXISTS users (
   id SERIAL PRIMARY KEY,
   user_id INT8 UNIQUE NOT NULL,
   username VARCHAR
);