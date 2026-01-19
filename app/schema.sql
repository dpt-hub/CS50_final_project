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
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);