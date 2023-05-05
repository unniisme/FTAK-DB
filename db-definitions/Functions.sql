-- Function and proceedure definitions

--Add all approved new products
--Note, this function only works if there is exactly 1 entry. So call it at each approval.
CREATE OR REPLACE PROCEDURE insert_approved_products() AS 
$$
DECLARE
  new_product_id INT;
BEGIN
  INSERT INTO product (name, description, rate, image_link)
  SELECT name, description, rate, image_link
  FROM new_product_approval
  WHERE approved = TRUE
  RETURNING product_id INTO new_product_id;
  
  INSERT INTO farmer_product_approval (farmer_id, product_id, quantity, depot_id, approved, entry_time)
  SELECT farmer_id, new_product_id, quantity, depot_id, FALSE, entry_time
  FROM new_product_approval
  WHERE approved = TRUE;

  DELETE FROM new_product_approval
  WHERE approved = TRUE;
END;
$$ LANGUAGE plpgsql;

-- get the farmer_product_id with the higest quantity of a given product. Returns None if None exists
CREATE OR REPLACE FUNCTION get_farmer_product_id(_product_id INT, _quantity INT)
RETURNS INT AS $$
DECLARE
  suitable_farmer_product_id INT;
BEGIN
  SELECT farmer_product_id FROM farmer_product fp WHERE fp.product_id = _product_id AND fp.quantity >= _quantity ORDER BY fp.quantity DESC LIMIT 1 INTO suitable_farmer_product_id;
  RETURN suitable_farmer_product_id;
END;
$$ LANGUAGE plpgsql;

-- Approve trade requests
CREATE OR REPLACE PROCEDURE insert_approved_trades() AS $$
DECLARE
    approved_rec RECORD;
    suitable_farmer_product_id INT;
    product_rate DECIMAL(10,2);
    product_depot_id INT;
BEGIN
    FOR approved_rec IN SELECT * FROM trade_request WHERE approved = TRUE LOOP
        SELECT get_farmer_product_id(approved_rec.product_id, approved_rec.quantity) INTO suitable_farmer_product_id;

        SELECT rate FROM product WHERE product.product_id = approved_rec.product_id INTO product_rate;
        SELECT depot_id FROM farmer_product WHERE farmer_product_id = suitable_farmer_product_id INTO product_depot_id;

        IF suitable_farmer_product_id IS NULL THEN
            RAISE WARNING 'No farmer has enough quantity of the product. Could not insert trade.';
            UPDATE trade_request SET approved = FALSE WHERE id = approved_rec.id;
        ELSE
          INSERT INTO trade (farmer_product_id, customer_id, quantity, depot_id, unit_rate, amount, rate) VALUES (suitable_farmer_product_id, approved_rec.customer_id, approved_rec.quantity, product_depot_id, product_rate, approved_rec.quantity * product_rate, product_rate);
        END IF;

    END LOOP;

    DELETE FROM trade_request WHERE approved = TRUE;
END;
$$ LANGUAGE plpgsql;


