-- We need to connect to tmp directory first
CREATE DATABASE bankdb;
\c bankdb

CREATE USER admin WITH PASSWORD 'admin';
GRANT ALL PRIVILEGES ON DATABASE bankdb TO admin;
GRANT ALL PRIVILEGES ON SCHEMA public TO admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE users TO admin;
-- Might just execute last one for all nto sure
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;

CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    password TEXT NOT NULL,
    dob DATE NOT NULL,
    address TEXT NOT NULL,
    CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    UNIQUE (email)
);

CREATE TABLE BankCard (
    CardID VARCHAR(9) PRIMARY KEY CHECK (CardID ~ '^\d{4} \d{4}$'),
    name VARCHAR(100) NOT NULL,
    expdate VARCHAR(7) NOT NULL CHECK (expdate ~ '^\d{4}-(0[1-9]|1[0-2])$'),
    cvv CHAR(3) NOT NULL CHECK (cvv ~ '^\d{3}$'),
    ownerID INTEGER NOT NULL,
    FOREIGN KEY (ownerID) REFERENCES Users(id)
);

CREATE TABLE Transactions (
    TransactionsID SERIAL PRIMARY KEY,
    source_CardID VARCHAR(9) CHECK (source_CardID ~ '^\d{4} \d{4}$'),
    target_CardID VARCHAR(9) CHECK (target_CardID ~ '^\d{4} \d{4}$'),
    transaction_type VARCHAR(50) NOT NULL CHECK (transaction_type IN ('Transfer', 'Deposit', 'Withdrawal')),
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, 
    FOREIGN KEY (source_CardID) REFERENCES BankCard(CardID),
    FOREIGN KEY (target_CardID) REFERENCES BankCard(CardID)
);
