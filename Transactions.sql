-- Use the existing database
USE shoppin_item;

-- Create the transactions table
CREATE TABLE Transactions (
    TransactionNumber INT AUTO_INCREMENT PRIMARY KEY,
    TransactionDateTime DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create the items table
CREATE TABLE TransactionItems (
    SerialNumber INT AUTO_INCREMENT PRIMARY KEY,
    TransactionNumber INT,
    ItemDescription VARCHAR(255),
    Price DECIMAL(10,2),
    FOREIGN KEY (TransactionNumber) REFERENCES Transactions(TransactionNumber)
);

-- Insert sample transaction data
INSERT INTO Transactions (TransactionDateTime) VALUES (NOW());

-- Get the last inserted transaction number
SET @LastTransaction = LAST_INSERT_ID();

-- Insert sample items for the transaction
INSERT INTO TransactionItems (TransactionNumber, ItemDescription, Price) VALUES
(@LastTransaction, 'Laptop', 1200.50),
(@LastTransaction, 'Mouse', 25.99),
(@LastTransaction, 'Keyboard', 45.00);

-- Select all transactions with their items
SELECT T.TransactionNumber, T.TransactionDateTime, TI.SerialNumber, TI.ItemDescription, TI.Price
FROM Transactions T
JOIN TransactionItems TI ON T.TransactionNumber = TI.TransactionNumber
ORDER BY T.TransactionNumber, TI.SerialNumber;
