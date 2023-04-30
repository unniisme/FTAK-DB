-- Function and proceedure definitions

--Transfer all approved requests to farmer-Plot
CREATE OR REPLACE FUNCTION approve_farmer_plot_requests()
  RETURNS VOID AS
$$
BEGIN
  -- Insert all approved requests into farmer_plot table
  INSERT INTO farmer_plot (farmer_id, plot_size, longitude, latitude)
  SELECT farmer_id, plot_size, longitude, latitude
  FROM farmer_plot_approval
  WHERE approved IS TRUE;

END;
$$
LANGUAGE plpgsql;

--Transfer all approved requests to farmer-depot
CREATE OR REPLACE PROCEDURE approve_farmer_depot_requests() AS 
$$
BEGIN
  INSERT INTO farmer_depot (farmer_id, depot_id)
  SELECT farmer_id, depot_id
  FROM farmer_product_approval
  WHERE approved IS TRUE;
END;
$$ LANGUAGE plpgsql;

--Transfer all approved requests to farmer-product and product table
CREATE OR REPLACE PROCEDURE approve_farmer_product_requests() AS
$$
    BEGIN
    INSERT INTO product (name, description, rate, image_link)
    SELECT name, description, rate, image_link
    FROM farmer_product_approval
    WHERE approved = true;


    INSERT INTO farmer_product (farmer_id, product_id, quantity, depot_id)
    SELECT farmer_id, product_id, quantity, depot_id
    FROM farmer_product_approval NATURAL JOIN product
    WHERE approved = true;
END;
$$ LANGUAGE plpgsql;


