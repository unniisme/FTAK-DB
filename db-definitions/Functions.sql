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

--Transfer all approved requests to farmer-product
CREATE OR REPLACE PROCEDURE approved_farmer_depot_requests() AS 
$$
BEGIN
  INSERT INTO farmer_depot (farmer_id, depot_id)
  SELECT farmer_id, depot_id
  FROM farmer_product_approval
  WHERE approved = TRUE;
END;
$$ LANGUAGE plpgsql;


