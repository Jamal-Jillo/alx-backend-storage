-- Name: items; Type: TABLE; Schema: public; Owner: postgres
CREATE TRIGGER decrease_quantity_trigger
AFTER INSERT ON orders
FOR EACH ROW
UPDATE items
SET quantity = quantity - NEW.quantity
WHERE id = NEW.item_id;
