drop table menu;

CREATE TABLE IF NOT EXISTS menu (
   img VARCHAR,
   name VARCHAR PRIMARY KEY,
   section VARCHAR,
   description VARCHAR,
   price INT8 NOT NULL
);