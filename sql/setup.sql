CREATE DATABASE testdb;
SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));

use testdb;

CREATE TABLE Brand (
    BrandID VARCHAR(36) PRIMARY KEY,
    BrandName VARCHAR(100),
    BrandDescription VARCHAR(1000)
);

CREATE TABLE Product (
    ProductID VARCHAR(36) PRIMARY KEY,
    ProductName VARCHAR(100),
    ProductPrice DECIMAL(10, 2),
    BrandID VARCHAR(36),
    FOREIGN KEY (BrandID) REFERENCES Brand(BrandID) ON DELETE CASCADE
);

CREATE TABLE Branch (
    BranchID VARCHAR(36) PRIMARY KEY,
    BranchName VARCHAR(100),
    Location VARCHAR(255)
);

CREATE TABLE Customer (
    CustomerID VARCHAR(36) PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Phone VARCHAR(20)
);

CREATE TABLE Employee (
    EmployeeID VARCHAR(36) PRIMARY KEY,
    Name VARCHAR(100),
    BranchID VARCHAR(36),
    FOREIGN KEY (BranchID) REFERENCES Branch(BranchID) ON DELETE CASCADE
);

CREATE TABLE `Order` (
    OrderID VARCHAR(36) PRIMARY KEY,
    ProductID VARCHAR(36),
    Quantity INT,
    CustomerID VARCHAR(36),
    OrderDate DATETIME,
    EmployeeID VARCHAR(36),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE CASCADE,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID) ON DELETE CASCADE
);

CREATE TABLE Shipping (
    ShippingID VARCHAR(36) PRIMARY KEY,
    OrderID VARCHAR(36),
    CarrierName VARCHAR(100),
    ShipDate DATETIME,
    FOREIGN KEY (OrderID) REFERENCES `Order`(OrderID) ON DELETE CASCADE
);
