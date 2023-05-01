-- Role and view definitions

--Create users
CREATE USER Farmer;

--Create views for Farmer
--Use python definitions instead
-- CREATE VIEW farmer_info AS
-- SELECT farmer.first_name, farmer.last_name, farmer.DoB, farmer.DoJ, farmer.phone_number, address.street_name, address.street_number, address.postal_code, city.name AS city_name, country.name AS country_name
-- FROM farmer
-- JOIN address ON farmer.address_id = address.address_id
-- JOIN city ON address.city_id = city.city_id
-- JOIN country ON address.country_id = country.country_id;

-- GRANT SELECT ON farmer_info TO Farmer;

GRANT INSERT ON farmer_plot_approval TO Farmer;
GRANT INSERT ON farmer_depot_approval TO Farmer;
GRANT INSERT ON farmer_product_approval TO Farmer;
GRANT SELECT ON product TO Farmer;
GRANT SELECT ON country TO Farmer;
GRANT SELECT ON city TO Farmer;
GRANT SELECT ON address TO Farmer;
GRANT SELECT ON depot TO Farmer;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public to Farmer;

--Supervisor
CREATE USER Supervisor;


--Create views for Supervisor
CREATE VIEW full_trade_data AS
SELECT trade.trade_id, farmer.first_name, farmer.last_name, product.name, trade.quantity, depot.name AS depot_name, trade.unit_rate, trade.rate
FROM trade
JOIN farmer_product ON trade.farmer_product_id = farmer_product.farmer_product_id
JOIN farmer ON farmer_product.farmer_id = farmer.farmer_id
JOIN depot ON trade.depot_id = depot.depot_id
JOIN product ON farmer_product.product_id = product.product_id;

CREATE VIEW farmer_depot_info AS
SELECT farmer.first_name, farmer.last_name, depot.name, address.street_name, address.street_number, address.postal_code, city.name AS city_name, country.name AS country_name
FROM farmer
JOIN farmer_depot ON farmer.farmer_id = farmer_depot.farmer_id
JOIN depot ON farmer_depot.depot_id = depot.depot_id
JOIN address ON depot.address_id = address.address_id
JOIN city ON address.city_id = city.city_id
JOIN country ON address.country_id = country.country_id;

GRANT SELECT ON full_trade_data TO Supervisor;
GRANT SELECT ON farmer_depot_info TO Supervisor;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO supervisor;
REVOKE INSERT, UPDATE, DELETE ON trade FROM supervisor;


-- Customer
CREATE USER Customer;

GRANT SELECT ON depot TO Customer;
GRANT SELECT ON product TO Customer;
GRANT SELECT ON address TO Customer;