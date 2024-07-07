use testdb;
SELECT Brand.BrandName, Product.ProductName, Product.ProductPrice
FROM Brand
JOIN Product on Product.BrandID = Brand.BrandID
WHERE Brand.BrandID = 1
