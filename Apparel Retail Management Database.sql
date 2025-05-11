-- Create the database
CREATE DATABASE ClothingShop;
GO

USE ClothingShop;
GO

-- 1. Users table
CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Name VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Password VARCHAR(100) NOT NULL,
    Role VARCHAR(10) CHECK (Role IN ('Admin', 'Customer')),
    Phone VARCHAR(15)
);

-- 2. Categories table
CREATE TABLE Categories (
    CategoryID INT PRIMARY KEY IDENTITY(1,1),
    CategoryName VARCHAR(50) NOT NULL
);

-- 3. Suppliers table
CREATE TABLE Suppliers (
    SupplierID INT PRIMARY KEY IDENTITY(1,1),
    SupplierName VARCHAR(100) NOT NULL,
    ContactNumber VARCHAR(15),
    Email VARCHAR(100)
);

-- 4. Products table
CREATE TABLE Products (
    ProductID INT PRIMARY KEY IDENTITY(1,1),
    ProductName VARCHAR(100) NOT NULL,
    CategoryID INT FOREIGN KEY REFERENCES Categories(CategoryID),
    SupplierID INT FOREIGN KEY REFERENCES Suppliers(SupplierID),
    Price DECIMAL(10,2) NOT NULL,
    Size VARCHAR(5),
    Color VARCHAR(20),
    Description TEXT
);

-- 5. Inventory table
CREATE TABLE Inventory (
    InventoryID INT PRIMARY KEY IDENTITY(1,1),
    ProductID INT FOREIGN KEY REFERENCES Products(ProductID),
    Quantity INT DEFAULT 0,
    LastUpdated DATE DEFAULT GETDATE()
);

-- 6. Orders table
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT FOREIGN KEY REFERENCES Users(UserID),
    OrderDate DATETIME DEFAULT GETDATE(),
    Status VARCHAR(20) DEFAULT 'Pending',
    TotalAmount DECIMAL(10,2)
);

-- 7. OrderItems table (for products in each order)
CREATE TABLE OrderItems (
    OrderItemID INT PRIMARY KEY IDENTITY(1,1),
    OrderID INT FOREIGN KEY REFERENCES Orders(OrderID),
    ProductID INT FOREIGN KEY REFERENCES Products(ProductID),
    Quantity INT,
    PriceAtOrder DECIMAL(10,2)
);

-- 8. Payments table
CREATE TABLE Payments (
    PaymentID INT PRIMARY KEY IDENTITY(1,1),
    OrderID INT FOREIGN KEY REFERENCES Orders(OrderID),
    Amount DECIMAL(10,2),
    PaymentMethod VARCHAR(20),
    PaymentDate DATETIME DEFAULT GETDATE()
);

-- 9. Shipping table
CREATE TABLE Shipping (
    ShippingID INT PRIMARY KEY IDENTITY(1,1),
    OrderID INT FOREIGN KEY REFERENCES Orders(OrderID),
    Address TEXT,
    City VARCHAR(50),
    PostalCode VARCHAR(10),
    Status VARCHAR(20) DEFAULT 'Processing'
);

-- 10. Reviews table
CREATE TABLE Reviews (
    ReviewID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT FOREIGN KEY REFERENCES Users(UserID),
    ProductID INT FOREIGN KEY REFERENCES Products(ProductID),
    Rating INT CHECK (Rating BETWEEN 1 AND 5),
    Comment TEXT,
    ReviewDate DATETIME DEFAULT GETDATE()
);

-- Insert sample users
INSERT INTO Users (Name, Email, Password, Role, Phone)
VALUES 
('Ali Raza', 'ali@example.com', 'securepass', 'Customer', '03001234567'),
('Sara Khan', 'sara@example.com', 'sara123', 'Customer', '03011234567'),
('Ahmed Malik', 'ahmed@example.com', 'ahmedpass', 'Admin', '03021234567'),
('Fatima Noor', 'fatima@example.com', 'fatimapass', 'Customer', '03031234567'),
('Usman Tariq', 'usman@example.com', 'usmanpass', 'Admin', '03041234567');

-- Insert categories
INSERT INTO Categories (CategoryName) 
VALUES ('Women'), ('Kids'), ('Men'), ('Accessories');

-- Insert suppliers
INSERT INTO Suppliers (SupplierName, ContactNumber, Email)
VALUES 
('Textile Express', '03005678901', 'contact@textileexpress.com'),
('Fashion Hub', '03015678901', 'info@fashionhub.com'),
('Premium Apparel', '03025678901', 'sales@premiumapparel.com'),
('Trendy Styles', '03035678901', 'support@trendystyles.com'),
('Urban Wear', '03045678901', 'contact@urbanwear.com');

-- Insert products (let IDENTITY handle the IDs)
INSERT INTO Products (ProductName, CategoryID, SupplierID, Price, Size, Color, Description)
VALUES
('Cotton T-Shirt', 3, 1, 1200.00, 'M', 'White', 'Premium quality cotton t-shirt for men'),
('Denim Jeans', 1, 2, 3500.00, 'L', 'Blue', 'Slim fit denim jeans for women'),
('Kids Jacket', 2, 3, 2500.00, 'S', 'Red', 'Warm jacket for children'),
('Silk Scarf', 4, 4, 1800.00, NULL, 'Multicolor', 'Luxury silk scarf'),
('Formal Shirt', 3, 5, 2800.00, 'XL', 'Black', 'Office wear formal shirt'),
('Summer Dress', 1, 1, 3200.00, 'M', 'Yellow', 'Lightweight summer dress'),
('Kids T-Shirt', 2, 2, 800.00, 'XS', 'Green', 'Comfortable cotton t-shirt for kids'),
('Leather Belt', 4, 3, 1500.00, NULL, 'Brown', 'Genuine leather belt'),
('Winter Coat', 1, 4, 5500.00, 'L', 'Navy Blue', 'Warm winter coat for women'),
('Sports Shorts', 3, 5, 1600.00, 'M', 'Gray', 'Breathable sports shorts');

-- Insert inventory directly with specified quantities
INSERT INTO Inventory (ProductID, Quantity)
VALUES
(1, 50),   -- Cotton T-Shirt
(2, 35),   -- Denim Jeans
(3, 20),   -- Kids Jacket
(4, 60),   -- Silk Scarf
(5, 40),   -- Formal Shirt
(6, 25),   -- Summer Dress
(7, 55),   -- Kids T-Shirt
(8, 30),   -- Leather Belt
(9, 15),   -- Winter Coat
(10, 45);  -- Sports Shorts

-- Insert orders (let IDENTITY handle the IDs)
INSERT INTO Orders (UserID, Status, TotalAmount)
VALUES
(1, 'Completed', 4700.00),
(2, 'Processing', 6300.00),
(3, 'Shipped', 4000.00),
(4, 'Pending', 2800.00),
(5, 'Completed', 8100.00);

-- Insert order items (reference existing products and orders)
INSERT INTO OrderItems (OrderID, ProductID, Quantity, PriceAtOrder)
VALUES
(1, (SELECT ProductID FROM Products WHERE ProductName = 'Cotton T-Shirt'), 2, 1200.00),
(1, (SELECT ProductID FROM Products WHERE ProductName = 'Leather Belt'), 1, 1500.00),
(1, (SELECT ProductID FROM Products WHERE ProductName = 'Sports Shorts'), 1, 1600.00),
(2, (SELECT ProductID FROM Products WHERE ProductName = 'Denim Jeans'), 1, 3500.00),
(2, (SELECT ProductID FROM Products WHERE ProductName = 'Summer Dress'), 1, 3200.00),
(3, (SELECT ProductID FROM Products WHERE ProductName = 'Kids Jacket'), 1, 2500.00),
(3, (SELECT ProductID FROM Products WHERE ProductName = 'Kids T-Shirt'), 2, 800.00),
(4, (SELECT ProductID FROM Products WHERE ProductName = 'Formal Shirt'), 1, 2800.00),
(5, (SELECT ProductID FROM Products WHERE ProductName = 'Silk Scarf'), 3, 1800.00),
(5, (SELECT ProductID FROM Products WHERE ProductName = 'Winter Coat'), 1, 5500.00);

-- Insert payments
INSERT INTO Payments (OrderID, Amount, PaymentMethod)
VALUES
(1, 4700.00, 'Credit Card'),
(2, 6300.00, 'JazzCash'),
(3, 4000.00, 'EasyPaisa'),
(4, 2800.00, 'Cash on Delivery'),
(5, 8100.00, 'Bank Transfer');

-- Insert shipping details
INSERT INTO Shipping (OrderID, Address, City, PostalCode, Status)
VALUES
(1, 'House 123, Street 45, Gulberg', 'Lahore', '54000', 'Delivered'),
(2, 'Flat 302, Eden Heights, DHA', 'Karachi', '75500', 'In Transit'),
(3, 'House 78, Street 12, F-7', 'Islamabad', '44000', 'Shipped'),
(4, 'Shop 5, Commercial Area, Bahria Town', 'Rawalpindi', '46000', 'Processing'),
(5, 'House 456, Street 9, Model Town', 'Lahore', '54000', 'Delivered');

-- Insert reviews
INSERT INTO Reviews (UserID, ProductID, Rating, Comment)
VALUES
(1, (SELECT ProductID FROM Products WHERE ProductName = 'Cotton T-Shirt'), 4, 'Good quality fabric but size was slightly small'),
(2, (SELECT ProductID FROM Products WHERE ProductName = 'Denim Jeans'), 5, 'Perfect fit and very comfortable'),
(3, (SELECT ProductID FROM Products WHERE ProductName = 'Kids Jacket'), 3, 'Good but color was not exactly as shown'),
(4, (SELECT ProductID FROM Products WHERE ProductName = 'Formal Shirt'), 4, 'Excellent formal shirt, worth the price'),
(5, (SELECT ProductID FROM Products WHERE ProductName = 'Winter Coat'), 5, 'Very warm and stylish coat'),
(1, (SELECT ProductID FROM Products WHERE ProductName = 'Leather Belt'), 2, 'Belt quality could be better'),
(2, (SELECT ProductID FROM Products WHERE ProductName = 'Summer Dress'), 4, 'Beautiful dress, received many compliments'),
(3, (SELECT ProductID FROM Products WHERE ProductName = 'Silk Scarf'), 5, 'Lovely scarf, great colors'),
(4, (SELECT ProductID FROM Products WHERE ProductName = 'Kids T-Shirt'), 3, 'Good for the price but stitching could be better'),
(5, (SELECT ProductID FROM Products WHERE ProductName = 'Sports Shorts'), 4, 'Comfortable and perfect for workouts');
 

 --1. Show all products with category and supplier names
SELECT p.ProductName, c.CategoryName, s.SupplierName, p.Price, p.Size, p.Color
FROM Products p
JOIN Categories c ON p.CategoryID = c.CategoryID
JOIN Suppliers s ON p.SupplierID = s.SupplierID;

--2. Display all orders with customer name and total amount
SELECT o.OrderID, u.Name AS CustomerName, o.OrderDate, o.TotalAmount, o.Status
FROM Orders o
JOIN Users u ON o.UserID = u.UserID;

--3. Show inventory status of all products
SELECT p.ProductName, i.Quantity, i.LastUpdated
FROM Inventory i
JOIN Products p ON i.ProductID = p.ProductID;

--4. Show all reviews for a specific product
SELECT r.Rating, r.Comment, u.Name AS Reviewer
FROM Reviews r
JOIN Users u ON r.UserID = u.UserID
WHERE r.ProductID = 1;

--5. Get total number of orders placed by each customer
SELECT u.Name, COUNT(o.OrderID) AS TotalOrders
FROM Users u
JOIN Orders o ON u.UserID = o.UserID
GROUP BY u.Name;


--6. Find top 5 best-selling products
SELECT p.ProductName, SUM(oi.Quantity) AS TotalSold
FROM OrderItems oi
JOIN Products p ON oi.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY TotalSold DESC
OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY;

--7. List all pending orders
SELECT OrderID, UserID, OrderDate, TotalAmount
FROM Orders
WHERE Status = 'Pending';

--8. Insert a new customer
INSERT INTO Users (Name, Email, Password, Role, Phone)
VALUES ('A.MUQEET', 'Muqeet@gmail.com', 'pass123', 'Customer', '03001234567');

select *from  Users 

--9. Update product stock in inventory
UPDATE Inventory
SET Quantity = Quantity - 2
WHERE ProductID = 3;

select *from  Inventory -----See Quantities of Stock

--10. Demonstrate Deletion Anomaly by Removing an Order
DELETE FROM OrderItems
WHERE OrderID = 4;

select * from OrderItems

--11. Show average rating for each product
SELECT p.ProductName, AVG(r.Rating) AS AvgRating
FROM Reviews r
JOIN Products p ON r.ProductID = p.ProductID
GROUP BY p.ProductName

--12. Show full shipping details for an order
SELECT s.ShippingID, s.Address, s.City, s.PostalCode, s.Status, o.OrderDate
FROM Shipping s
JOIN Orders o ON s.OrderID = o.OrderID
WHERE s.OrderID = 2;

--13. List all payments made using 'Card' method
SELECT * FROM Payments
WHERE PaymentMethod = 'Cash on delivery';

--14. Get total sales (revenue)
SELECT SUM(Amount) AS TotalSales
FROM Payments;

--15. List all customers who have not placed any order
SELECT Name, Email
FROM Users
WHERE Role = 'Customer'
  AND UserID NOT IN (
    SELECT DISTINCT UserID FROM Orders
    WHERE UserID IS NOT NULL
);

SELECT * FROM Users WHERE Role = 'Admin';
SELECT * FROM Users WHERE Role = 'Customer';


--16. Show product details with inventory status below threshold (e.g., < 5)
SELECT p.ProductName, i.Quantity
FROM Products p
JOIN Inventory i ON p.ProductID = i.ProductID
WHERE i.Quantity < 45;