-- Function and proceedure definitions

--Add all approved new products
CREATE OR REPLACE PROCEDURE insert_approved_products() AS 
$$
BEGIN
  INSERT INTO product (name, description, rate, image_link)
  SELECT name, description, rate, image_link
  FROM new_product_approval
  WHERE approved = TRUE;

  DELETE FROM new_product_approval
  WHERE approved = TRUE;
END;
$$ LANGUAGE plpgsql;

-- get the farmer_product_id with the higest quantity of a given product. Returns None if None exists
CREATE OR REPLACE FUNCTION get_farmer_product_ids(_product_id INT, _quantity INT)
RETURNS INT AS $$
DECLARE
  suitable_farmer_product_id INT;
BEGIN
  SELECT farmer_product_id FROM farmer_product fp WHERE fp.product_id = _product_id AND fp.quantity < _quantity ORDER BY fp.quantity ASC LIMIT 1 INTO suitable_farmer_product_id;
  RETURN suitable_farmer_product_id;
END;
$$ LANGUAGE plpgsql;

-- Approve trade requests
CREATE OR REPLACE PROCEDURE insert_approved_trades() AS $$
DECLARE
    approved_rec RECORD;
    suitable_farmer_product_id INT;
    product_rate DECIMAL(10,2);
BEGIN
    FOR approved_rec IN SELECT * FROM trade_request WHERE approved = TRUE LOOP
        SELECT rate FROM product WHERE product.product_id = approved_rec.product_id INTO product_rate;

        SELECT get_farmer_product_id(approved_rec.product_id, approved_rec.quantity) INTO suitable_farmer_product_id;

        IF suitable_farmer_product_id IS NULL THEN
            RAISE EXCEPTION 'No farmer has enough quantity of the product. Could not insert trade.';
        END IF;

        INSERT INTO trade (farmer_product_id, customer_id, quantity, depot_id, unit_rate, amount, rate) VALUES (suitable_farmer_product_id, approved_rec.customer_id, approved_rec.quantity, approved_rec.depot_id, approved_rec.unit_rate, approved_rec.quantity * approved_rec.unit_rate, product_rate);
    END LOOP;
END;
$$ LANGUAGE plpgsql;


