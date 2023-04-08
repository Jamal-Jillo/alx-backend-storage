-- Creates a trigger that resets the valid_email field
CREATE TRIGGER reset_valid_email AFTER UPDATE ON users
FOR EACH ROW
BEGIN
  IF NEW.email <> OLD.email THEN
    UPDATE users SET valid_email = NULL WHERE id = NEW.id;
  ELSE
    SET NEW.valid_email = OLD.valid_email;
  END IF;
END;
