-- Create a table users with the following fields:
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email UNIQUE VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    country CHAR(2) NOT NULL DEFAULT 'US' CHECK (country IN ('US', 'CO', 'TN')),
    );
