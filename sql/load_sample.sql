USE testdb;

LOAD DATA LOCAL
INFILE 'sample_data/sample_branch.csv'
INTO TABLE Branch
FIELDS TERMINATED BY ','
ENCLOSED BY ""
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL
INFILE 'sample_data/sample_brand.csv'
INTO TABLE Brand
FIELDS TERMINATED BY ','
ENCLOSED BY ""
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL
INFILE 'sample_data/sample_customer.csv'
INTO TABLE Customer
FIELDS TERMINATED BY ','
ENCLOSED BY ""
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL
INFILE 'sample_data/sample_employee.csv'
INTO TABLE Employee
FIELDS TERMINATED BY ','
ENCLOSED BY ""
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL
INFILE 'sample_data/sample_order.csv'
INTO TABLE `Order`
FIELDS TERMINATED BY ','
ENCLOSED BY ""
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL
INFILE 'sample_data/sample_product.csv'
INTO TABLE Product
FIELDS TERMINATED BY ','
ENCLOSED BY ""
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL
INFILE 'sample_data/sample_shipping.csv'
INTO TABLE Shipping
FIELDS TERMINATED BY ','
ENCLOSED BY ""
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
