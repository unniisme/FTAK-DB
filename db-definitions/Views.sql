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
CREATE VIEW trade_info AS
SELECT t.trade_id, f.first_name || ' ' || f.last_name as farmer_name, t.quantity, p.name as product_name, d.name as depot_name, t.unit_rate, t.rate, c.first_name || ' ' || c.last_name as customer_name, t.amount as total_amount
FROM trade t JOIN farmer_product fp ON t.farmer_product_id = fp.farmer_product_id
    JOIN farmer f ON f.farmer_id = fp.farmer_id
    JOIN product p ON p.product_id = fp.product_id
    JOIN depot d ON t.depot_id = d.depot_id
    JOIN customer c ON c.customer_id = t.customer_id;


CREATE VIEW farmer_depot_info AS
SELECT farmer.first_name, farmer.last_name, depot.name, address.street_name, address.street_number, address.postal_code, city.name AS city_name, country.name AS country_name
FROM farmer
JOIN farmer_depot ON farmer.farmer_id = farmer_depot.farmer_id
JOIN depot ON farmer_depot.depot_id = depot.depot_id
JOIN address ON depot.address_id = address.address_id
JOIN city ON address.city_id = city.city_id
JOIN country ON address.country_id = country.country_id;

GRANT SELECT ON trade_info TO Supervisor;
GRANT SELECT ON farmer_depot_info TO Supervisor;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO supervisor;
REVOKE INSERT, UPDATE, DELETE ON trade FROM supervisor;


-- Customer
CREATE USER Customer;

GRANT SELECT ON depot TO Customer;
GRANT SELECT ON product TO Customer;
GRANT SELECT ON address TO Customer;
GRANT INSERT ON trade_request TO Customer;
GRANT USAGE, SELECT ON trade_request_id_seq TO Customer;
