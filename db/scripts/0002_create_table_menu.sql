drop table menu;

CREATE TABLE IF NOT EXISTS menu (
   id SERIAL PRIMARY KEY,
   img VARCHAR UNIQUE,
   name VARCHAR UNIQUE,
   section VARCHAR,
   description VARCHAR,
   price INT8 NOT NULL
);