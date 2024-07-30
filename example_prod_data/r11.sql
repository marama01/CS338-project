use testdb;
SELECT Brand.BrandName, COUNT(Product.ProductID), AVG(Product.ProductPrice)
FROM Brand
JOIN Product ON Product.BrandID = Brand.BrandID
GROUP BY Brand.BrandID
