CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL
);

CREATE TABLE clients (
    client_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    address TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);

CREATE TABLE visits (
    visit_id INTEGER PRIMARY KEY,
    client_id INTEGER,
    date DATETIME NOT NULL,
    order_value INTEGER NOT NULL
);