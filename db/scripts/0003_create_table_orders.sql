drop table orders;

CREATE TABLE IF NOT EXISTS orders (
   id SERIAL PRIMARY KEY,
   menu_id INT8 UNIQUE NOT NULL,
   user_id INT8 UNIQUE NOT NULL,
   amount INT8
);