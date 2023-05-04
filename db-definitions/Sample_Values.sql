-- Some sample values in the database

-- Insert data into country table
INSERT INTO country (name) 
VALUES ('Canada'), ('USA'), ('Mexico'), ('India');

-- Insert data into city table
INSERT INTO city (name, country_id) 
VALUES ('Vancouver',1), ('Toronto',1), ('Montreal',1), ('Los Angeles',2), ('New York',2), ('Chicago',2), ('Mexico City',3), ('Guadalajara',3);
INSERT INTO city (country_id, name)
VALUES (1, 'Thiruvananthapuram'),
       (1, 'Kochi'),
       (1, 'Kozhikode');




-- Insert data into address table
INSERT INTO address (street_name, street_number, postal_code, city_id, country_id)
VALUES ('123 Main St', 'Suite 340', 'V6A 2T9', 1, 1),
       ('500 Queens Quay', 'Unit 20', 'M5V 2Y3', 1, 1),
       ('12 Rue Sainte-Catherine', '', 'H2X 1Z5', 3, 1);
INSERT INTO address (city_id, country_id, street_name, street_number, postal_code)
VALUES (1, 1, 'MG Road', '34A', '695001'),
       (2, 1, 'Banerji Road', '2B', '682101'),
       (3, 1, 'Court Road', '25', '673001');


-- Insert data into farmer table -- Use python signup instead
-- INSERT INTO farmer (first_name, last_name, DoB, DoJ, phone_number, address_id)
-- VALUES ('John', 'Doe', '1987-05-12', '2012-04-01', '555-555-5555', 1),
--        ('Jane', 'Smith', '1990-02-15', '2015-01-01', '777-777-7777', 2),
--        ('Alberto', 'Garcia', '1985-11-22', '2014-07-01', '111-111-1111', 3);


-- Insert data into farmer_plot table -- Use request from farmer instead
-- INSERT INTO farmer_plot (farmer_id, plot_size, longitude, latitude)
-- VALUES (1, 10, -123.123, 49.234),
--        (1, 20, -123.124, 49.233),
--        (2, 15, -79.393, 43.659),
--        (3, 8, -99.143, 19.433);


-- Insert data into product table
INSERT INTO product (name, description, rate, image_link)
VALUES ('Apples', 'Fresh and delicious', 1.99, 'https://example.com/apples.jpg'),
       ('Oranges', 'Juicy and sweet', 2.49, 'https://example.com/oranges.jpg'),
       ('Tomatoes', 'Bright and flavourful', 0.99, 'https://example.com/tomatoes.jpg'),
       ('Organic Carrots', 'Crunchy and sweet organic carrots, great for snacking', 1.50, 'https://example.com/carrot-image.jpg');


-- Insert data into depot table
INSERT INTO depot (name, address_id)
VALUES ('Farmers Market', 2),
       ('Grocery Store', 1),
       ('Big Box Store', 3),
       ('Kayal Store', 5),
       ('Green Market', 6);


-- Insert data into farmer_product table -- Use farmer request
-- INSERT INTO farmer_product (farmer_id, product_id, quantity, depot_id)
-- VALUES (1, 1, 100, 1),
--        (2, 2, 75, 1),
--        (1, 3, 50, 2),
--        (3, 1, 30, 3),
--        (3, 3, 20, 3);


-- Insert data into farmer_depot table -- Use farmer request
-- INSERT INTO farmer_depot (farmer_id, depot_id)
-- VALUES (1, 1),
--        (1, 2),
--        (2, 1),
--        (3, 3);