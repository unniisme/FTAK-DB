-- Role and view definitions

--Create users
CREATE USER Farmer;
CREATE USER Supervisor;

--Create views for Farmer
CREATE VIEW farmer_info AS
SELECT farmer.first_name, farmer.last_name, farmer.DoB, farmer.DoJ, farmer.phone_number, address.street_name, address.street_number, address.postal_code, city.name AS city_name, country.name AS country_name
FROM farmer
JOIN address ON farmer.address_id = address.address_id
JOIN city ON address.city_id = city.city_id
JOIN country ON address.country_id = country.country_id;

CREATE VIEW farmer_product_info AS
SELECT farmer.first_name, farmer.last_name, product.name, farmer_product.quantity
FROM farmer
JOIN farmer_product ON farmer.farmer_id = farmer_product.farmer_id
JOIN product ON farmer_product.product_id = product.product_id;

GRANT SELECT ON farmer_info TO Farmer;
GRANT SELECT ON farmer_product_info TO Farmer;

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