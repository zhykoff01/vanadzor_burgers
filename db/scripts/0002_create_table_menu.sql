drop table menu;

CREATE TABLE IF NOT EXISTS menu (
   img VARCHAR,
   name VARCHAR PRIMARY KEY,
   description VARCHAR,
   price INT8 NOT NULL
);