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
