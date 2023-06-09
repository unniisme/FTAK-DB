-- Table definitions
-- DB name is ftak

-- CREATE DATABASE ftak;

CREATE TABLE farmer (
  farmer_id SERIAL,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  DoB DATE NOT NULL,
  DoJ DATE NOT NULL,
  phone_number VARCHAR(20) NOT NULL,
  address_id INT NOT NULL,
  PRIMARY KEY (farmer_id)
);

CREATE TABLE farmer_plot (
  plot_id SERIAL,
  farmer_id INT NOT NULL,
  plot_size INT NOT NULL,
  longitude NUMERIC NOT NULL,
  latitude NUMERIC NOT NULL,
  PRIMARY KEY (plot_id),
  FOREIGN KEY (farmer_id) REFERENCES farmer (farmer_id)
);

CREATE TABLE product (
  product_id SERIAL,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  rate DECIMAL(10,2) NOT NULL,
  image_link VARCHAR(50),
  PRIMARY KEY (product_id)
);

CREATE TABLE farmer_product (
  farmer_product_id SERIAL,
  farmer_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  depot_id INT NOT NULL,
  PRIMARY KEY (farmer_product_id),
  FOREIGN KEY (farmer_id) REFERENCES farmer (farmer_id),
  FOREIGN KEY (product_id) REFERENCES product (product_id)
);

CREATE TABLE depot (
  depot_id SERIAL,
  name VARCHAR(100) NOT NULL,
  address_id INT NOT NULL,
  PRIMARY KEY (depot_id)
);

CREATE TABLE farmer_depot (
  farmer_depot_id SERIAL,
  farmer_id INT NOT NULL,
  depot_id INT NOT NULL,
  PRIMARY KEY (farmer_depot_id),
  FOREIGN KEY (farmer_id) REFERENCES farmer (farmer_id),
  FOREIGN KEY (depot_id) REFERENCES depot (depot_id)
);

CREATE TABLE trade (
  trade_id SERIAL,
  farmer_product_id INT NOT NULL,
  customer_id INT NOT NULL,  --ALTER TABLE trade ADD COLUMN customer_id INT NOT NULL;
  quantity INT NOT NULL,
  depot_id INT NOT NULL,
  unit_rate DECIMAL(10,2) NOT NULL,
  amount DECIMAL(10, 2) NOT NULL, --ALTER TABLE trade ADD COLUMN amount DECIMAL(10, 2) NOT NULL
  rate DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (trade_id)
);

CREATE TABLE address (
  address_id SERIAL,
  city_id INT NOT NULL,
  country_id INT NOT NULL,
  street_name VARCHAR(100) NOT NULL,
  street_number VARCHAR(20),
  postal_code VARCHAR(20),
  PRIMARY KEY (address_id)
);

CREATE TABLE country (
  country_id SERIAL,
  name VARCHAR(100) NOT NULL,
  PRIMARY KEY (country_id)
);

CREATE TABLE city (
  city_id SERIAL,
  country_id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  PRIMARY KEY (city_id)
);

CREATE TABLE customer (
  customer_id SERIAL UNIQUE,
  customer_username VARCHAR(50) NOT NULL UNIQUE,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL,
  phone_number VARCHAR(20) NOT NULL,
  PRIMARY KEY (customer_id, customer_username)
);


ALTER TABLE farmer ADD CONSTRAINT address_fk FOREIGN KEY (address_id) REFERENCES address (address_id);
ALTER TABLE farmer_product ADD CONSTRAINT farmer_fk FOREIGN KEY (farmer_id) REFERENCES farmer (farmer_id);
ALTER TABLE farmer_product ADD CONSTRAINT product_fk FOREIGN KEY (product_id) REFERENCES product (product_id);
ALTER TABLE depot ADD CONSTRAINT address_fk FOREIGN KEY (address_id) REFERENCES address (address_id);
ALTER TABLE farmer_depot ADD CONSTRAINT farmer_fk FOREIGN KEY (farmer_id) REFERENCES farmer (farmer_id);
ALTER TABLE farmer_depot ADD CONSTRAINT depot_fk FOREIGN KEY (depot_id) REFERENCES depot (depot_id);
ALTER TABLE trade ADD CONSTRAINT fp_fk FOREIGN KEY (farmer_product_id) REFERENCES farmer_product (farmer_product_id);
ALTER TABLE trade ADD CONSTRAINT depot_fk FOREIGN KEY (depot_id) REFERENCES depot (depot_id);
ALTER TABLE address ADD CONSTRAINT city_fk FOREIGN KEY (city_id) REFERENCES city (city_id);
ALTER TABLE address ADD CONSTRAINT country_fk FOREIGN KEY (country_id) REFERENCES country (country_id);
ALTER TABLE city ADD CONSTRAINT country_fk FOREIGN KEY (country_id) REFERENCES country (country_id);
ALTER TABLE trade ADD CONSTRAINT customer_fk FOREIGN KEY (customer_id) REFERENCES customer (customer_id);


-- Logins
CREATE TABLE farmer_login (
  username VARCHAR(100) PRIMARY KEY,
  farmer_id INT NOT NULL,

  FOREIGN KEY (farmer_id) REFERENCES farmer (farmer_id)
);

--A log of requests a farmer can make to farmer_plot table. Each entry in this table has to be approved by a supervisor to be added to farmer plot table
CREATE TABLE farmer_plot_approval (
  id SERIAL PRIMARY KEY,
  farmer_id INT NOT NULL,
  plot_size INT NOT NULL,
  longitude NUMERIC NOT NULL,
  latitude NUMERIC NOT NULL,
  FOREIGN KEY (farmer_id) REFERENCES farmer (farmer_id),

  approved BOOLEAN NOT NULL,
  entry_time timestamp
);

--Similar log for farmer_depot
CREATE TABLE farmer_depot_approval (
  id SERIAL PRIMARY KEY,
  farmer_id INT NOT NULL,
  depot_id INT NOT NULL,
  FOREIGN KEY (farmer_id) REFERENCES farmer (farmer_id),
  FOREIGN KEY (depot_id) REFERENCES depot (depot_id),

  approved BOOLEAN NOT NULL,
  entry_time timestamp
);

--Similar for farmer product
CREATE TABLE farmer_product_approval (
  id SERIAL PRIMARY KEY,

  farmer_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  depot_id INT NOT NULL,
  FOREIGN KEY (farmer_id) REFERENCES farmer (farmer_id),
  FOREIGN KEY (product_id) REFERENCES product (product_id),
  FOREIGN KEY (depot_id) REFERENCES depot (depot_id),

  approved BOOLEAN NOT NULL,
  entry_time timestamp
);

CREATE TABLE new_product_approval (
  id SERIAL PRIMARY KEY,

  farmer_id INT NOT NULL, 
  name VARCHAR(100) NOT NULL,
  description TEXT,
  rate DECIMAL(10,2) NOT NULL,
  image_link VARCHAR,

  quantity INT NOT NULL,
  depot_id INT NOT NULL,

  FOREIGN KEY (farmer_id) REFERENCES farmer (farmer_id),
  FOREIGN KEY (depot_id) REFERENCES depot (depot_id),

  approved BOOLEAN NOT NULL,
  entry_time timestamp
);

CREATE TABLE trade_request (
  id SERIAL PRIMARY KEY,
  customer_id INT NOT NULL,
  product_id INT NOT NULL, 
  quantity INT NOT NULL,

  FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
  FOREIGN KEY (product_id) REFERENCES product (product_id),

  approved BOOLEAN NOT NULL,
  entry_time timestamp
);
