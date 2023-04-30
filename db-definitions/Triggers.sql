--Trigger definitions

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