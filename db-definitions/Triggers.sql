--Trigger definitions

-- Farmer plot approval
CREATE OR REPLACE FUNCTION approve_farmer_plot_requests() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.approved THEN
        INSERT INTO farmer_plot (farmer_id, plot_size, longitude, latitude)
        VALUES (NEW.farmer_id, NEW.plot_size, NEW.longitude, NEW.latitude);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER approve_farmer_plot_trigger
    AFTER UPDATE OF approved ON farmer_plot_approval
    FOR EACH ROW
    EXECUTE FUNCTION approve_farmer_plot_requests();

--Farmer Depot approval
CREATE OR REPLACE FUNCTION approve_farmer_depot_requests() RETURNS TRIGGER AS $$ 
BEGIN
  IF NEW.approved THEN
    INSERT INTO farmer_depot (farmer_id, depot_id)
    VALUES (NEW.farmer_id, NEW.depot_id);
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER approve_farmer_depot_trigger
    AFTER UPDATE OF approved ON farmer_depot_approval
    FOR EACH ROW
    EXECUTE FUNCTION approve_farmer_depot_requests();

-- Farmer Product approval
CREATE OR REPLACE FUNCTION approve_farmer_product_requests() RETURNS TRIGGER AS $$ 
BEGIN
  IF NEW.approved THEN
    IF EXISTS (SELECT * FROM farmer_depot WHERE farmer_id = NEW.farmer_id AND depot_id = NEW.depot_id) THEN
        INSERT INTO farmer_product (farmer_id, product_id, quantity, depot_id)
        VALUES (NEW.farmer_id, NEW.product_id, NEW.quantity, NEW.depot_id);
    ELSE
        RAISE EXCEPTION 'Farmer-depot combination is not valid.';
        UPDATE farmer_product_approval SET approved = FALSE WHERE id = NEW.id;
    END IF;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER approve_farmer_product_trigger
    AFTER UPDATE OF approved ON farmer_product_approval
    FOR EACH ROW
    EXECUTE FUNCTION approve_farmer_product_requests();


-- Trade quantity
CREATE OR REPLACE FUNCTION check_trade_quantity() 
RETURNS TRIGGER AS 
$$
DECLARE
    product_quantity INT;
BEGIN
    SELECT quantity INTO product_quantity FROM farmer_product 
    WHERE farmer_product_id = NEW.farmer_product_id AND depot_id = NEW.depot_id;
    
    IF NEW.quantity > product_quantity THEN
        RAISE EXCEPTION 'Trade quantity cannot be greater than product quantity';
    ELSE
        -- Decrease the quantity in the farmer_product table
        UPDATE farmer_product 
        SET quantity = quantity - NEW.quantity 
        WHERE farmer_product_id = NEW.farmer_product_id AND depot_id = NEW.depot_id;
        RETURN NEW;
    END IF;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER check_trade_quantity_trigger 
BEFORE INSERT ON trade 
FOR EACH ROW 
EXECUTE FUNCTION check_trade_quantity();
--