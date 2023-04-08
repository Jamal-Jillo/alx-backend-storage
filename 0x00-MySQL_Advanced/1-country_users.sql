-- Create a table users with the following fields:
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    country ENUM('US', 'CA', 'TN') NOT NULL DEFAULT 'US'
    );
