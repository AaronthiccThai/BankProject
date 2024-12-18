CREATE DATABASE bankdb;
\c bankdb

CREATE USER admin WITH PASSWORD 'admin';
GRANT ALL PRIVILEGES ON DATABASE bankdb TO admin;
GRANT ALL PRIVILEGES ON SCHEMA public TO admin;

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
    CardID SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    expdate DATE NOT NULL,
    cvv CHAR(3) NOT NULL CHECK (cvv ~ '^\d{3}$'),
    ownerID INTEGER NOT NULL,
    FOREIGN KEY (ownerID) REFERENCES Users(id)
);

CREATE TABLE Transactions (
    TransactionsID SERIAL PRIMARY KEY,
    source_CardID INTEGER NOT NULL,
    target_CardID INTEGER NOT NULL,
    transaction_type VARCHAR(50) NOT NULL CHECK (transaction_type IN ('Transfer', 'Deposit', 'Withdrawal')),
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    FOREIGN KEY (source_CardID) REFERENCES BankCard(CardID),
    FOREIGN KEY (target_CardID) REFERENCES BankCard(CardID)
);
