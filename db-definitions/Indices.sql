-- Index definitions

-- B-tree index on the farmer table to speed up search by name:
CREATE INDEX farmer_name_idx ON farmer (name);
CREATE INDEX farmer_username_idx ON farmer_login (username);

-- Hash index on the farmer_depot table to speed up search by both farmer_id and depot_id:
CREATE INDEX farmer_depot_farmer_id_depot_id_idx ON farmer_depot USING hash (farmer_id, depot_id);

-- Partial index on the farmer_product table to index only rows where quantity is greater than zero:
CREATE INDEX farmer_product_quantity_gt_zero_idx ON farmer_product (farmer_id, product_id) WHERE quantity > 0;


