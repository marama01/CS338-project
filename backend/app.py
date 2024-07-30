from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS
import json
import logging
import datetime

app = Flask(__name__)
CORS(app)

logging.basicConfig(filename='record.log', level=logging.DEBUG)

def convertTime(s):
    return datetime.datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %Z").strftime('%Y-%m-%d %H:%M:%S')

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="testdb"
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

@app.route('/brand', methods=['GET'])
def get_brands():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Brand")
        rows = cursor.fetchall()
        jrows = jsonify(rows)
        app.logger.info("Fetching brand")
        app.logger.info(jrows)
        return jrows

@app.route('/brand-summary/', methods=['GET'])
def getBrandSummary():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT Brand.BrandName, COUNT(Product.ProductID), AVG(Product.ProductPrice) \
              FROM Brand \
              JOIN Product ON Product.BrandID = Brand.BrandID \
              GROUP BY Brand.BrandID"
    cursor.execute(query)
    rows = cursor.fetchall()
    jrows = jsonify(rows)
    app.logger.info(jrows)
    return jrows

@app.route('/brand/<id>', methods=['GET', 'POST', 'DELETE'])
def brandId(id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'GET':
        # TODO: Modify this to fetch only id
        query = "SELECT Brand.BrandName, Product.ProductName, Product.ProductPrice \
                 FROM Brand \
                 JOIN Product on Product.BrandID = Brand.BrandID \
                 WHERE Brand.BrandID = %s"
        cursor.execute(query, (id,))
        rows = cursor.fetchall()
        jrows = jsonify(rows)
        app.logger.info(jrows)
        return jrows
    elif request.method == 'POST':
        app.logger.info("Updating Brand")
        data = request.form
        brandID = data["BrandID"]
        brandName = data["BrandName"]
        brandDescription = data["BrandDescription"]
        query = f"SELECT * FROM Brand WHERE BrandID = '{brandID}'"
        cursor.execute(query)
        app.logger.info(query)
        res = cursor.fetchone()
        if res is None:
            app.logger.info("Adding the following to brand table:")
            app.logger.info("BrandId: " + brandID)
            app.logger.info("BrandName: " + brandName)
            query = f"INSERT INTO Brand (BrandID, BrandName, BrandDescription) VALUES (%s, %s, %s)"
            app.logger.info("query:" + query)
            cursor.execute(query, (brandID, brandName, brandDescription))
            connection.commit()
            ret = cursor.fetchall()
            return jsonify(ret)
        else:
            app.logger.info("Updating the following to brand table:")
            app.logger.info("BrandId: " + brandID)
            app.logger.info("BrandName: " + brandName)

            query = f"UPDATE Brand SET BrandName = %s, BrandDescription = %s WHERE BrandID = %s"
            app.logger.info("query:" + query)
            cursor.execute(query, (brandName, brandDescription, brandID))
            connection.commit()
            return cursor.rowcount

    elif request.method == 'DELETE':
        app.logger.info("Deleting Brand")
        data = request.form
        brandID = data["BrandID"]
        query = f"DELETE FROM Brand WHERE BrandID = %s"
        app.logger.info("query:" + query)
        try:
            cursor.execute(query, (brandID,))
            connection.commit()
            ret = cursor.fetchall()
            return jsonify(ret)
        except get_mysql_exception:
            return "Unable to delete. (Probably due to deleting an entry where a foreign key is needed.)"

@app.route('/product', methods=['GET'])
def get_products():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Product")
        rows = cursor.fetchall()
        jrows = jsonify(rows)
        app.logger.info("Fetching product")
        app.logger.info(jrows)
        return jrows

@app.route('/product-summary/', methods=['GET'])
def getProductSummary():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT AVG(Product.ProductPrice) \
              FROM Product"
    cursor.execute(query)
    rows = cursor.fetchall()
    jrows = jsonify(rows)
    app.logger.info(jrows)
    return jrows

@app.route('/product/<id>', methods=['GET', 'POST', 'DELETE'])
def productId(id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    #app.logger.info("In /brands/", id)
    if request.method == 'GET':
        # TODO: Modify this to fetch only id
        query = "SELECT Brand.BrandName, Product.ProductName, Product.ProductPrice \
                 FROM Brand \
                 JOIN Product on Product.BrandID = Brand.BrandID \
                 WHERE Product.ProductID = %s"
        cursor.execute(query, (id,))
        rows = cursor.fetchall()
        jrows = jsonify(rows)
        app.logger.info(jrows)
        return jrows
    elif request.method == 'POST':
        app.logger.info("Updating Product")
        data = request.form
        ProductID = data["ProductID"]
        BrandID = data["BrandID"]
        ProductName = data["ProductName"]
        ProductPrice = data["ProductPrice"]
        query = f"SELECT * FROM Product WHERE ProductID = '{ProductID}'"
        cursor.execute(query)
        app.logger.info(query)
        res = cursor.fetchone()
        if res is None:
            query = f"INSERT INTO Product (BrandID, ProductID, ProductName, ProductPrice) VALUES (%s, %s, %s, %s)"
            app.logger.info("query:" + query)
            cursor.execute(query, (BrandID, ProductID, ProductName, ProductPrice))
            connection.commit()
            ret = cursor.fetchall()
            return jsonify(ret)
        else:
            query = f"UPDATE Product SET ProductName = %s, BrandID = %s, ProductPrice = %s WHERE ProductID = %s"
            app.logger.info("query:" + query)
            cursor.execute(query, (ProductName, BrandID, ProductPrice, ProductID))
            connection.commit()
            return cursor.rowcount

    elif request.method == 'DELETE':
        app.logger.info("Deleting Brand")
        data = request.form
        ProductID = data["ProductID"]
        query = f"DELETE FROM Product WHERE ProductID = %s"
        app.logger.info("query:" + query)
        try:
            cursor.execute(query, (ProductID,))
            connection.commit()
            ret = cursor.fetchall()
            return jsonify(ret)
        except get_mysql_exception:
            return "Unable to delete. (Probably due to deleting an entry where a foreign key is needed.)"

@app.route('/branch', methods=['GET'])
def get_branchs():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Branch")
        rows = cursor.fetchall()
        jrows = jsonify(rows)
        app.logger.info("Fetching branch")
        app.logger.info(jrows)
        return jrows

@app.route('/branch-summary/', methods=['GET'])
def getBranchSummary():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * \
              FROM Branch \
              JOIN Employee ON Employee.BranchID = Branch.BranchID \
              GROUP BY Branch.BranchID"
    cursor.execute(query)
    rows = cursor.fetchall()
    jrows = jsonify(rows)
    app.logger.info(jrows)
    return jrows

@app.route('/branch/<id>', methods=['GET', 'POST', 'DELETE'])
def branchId(id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'GET':
        # TODO: Modify this to fetch only id
        query = "SELECT * \
                FROM Branch \
                JOIN Employee ON Employee.BranchID = Branch.BranchID \
                WHERE Branch.BranchID=%s"
        cursor.execute(query, (id,))
        rows = cursor.fetchall()
        jrows = jsonify(rows)
        app.logger.info(jrows)
        return jrows
    elif request.method == 'POST':
        app.logger.info("Updating Branch")
        data = request.form
        BranchID = data["BranchID"]
        BranchName = data["BranchName"]
        Location = data["Location"]
        app.logger.info(BranchID)
        query = f"SELECT * FROM Branch WHERE BranchID = %s"
        cursor.execute(query, (BranchID,))
        app.logger.info(query)
        res = cursor.fetchone()
        if res is None:
            query = f"INSERT INTO Branch (BranchID, BranchName, Location) VALUES (%s, %s, %s)"
            app.logger.info("query:" + query)
            cursor.execute(query, (BranchID, BranchName, Location))
            connection.commit()
            ret = cursor.fetchall()
            return jsonify(ret)
        else:
            query = f"UPDATE Branch SET BranchName = %s, Location = %s WHERE BranchID = %s"
            app.logger.info("query:" + query)
            cursor.execute(query, (BranchName, Location, BranchID))
            connection.commit()
            return cursor.rowcount

    elif request.method == 'DELETE':
        data = request.form
        BranchID = data["BranchID"]
        query = f"DELETE FROM Branch WHERE BranchID = %s"
        app.logger.info("query:" + query)
        try:
            cursor.execute(query, (BranchID,))
            connection.commit()
            ret = cursor.fetchall()
            return jsonify(ret)
        except get_mysql_exception:
            return "Unable to delete. (Probably due to deleting an entry where a foreign key is needed.)"

@app.route('/employee', methods=['GET'])
def get_employees():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Employee")
        rows = cursor.fetchall()
        jrows = jsonify(rows)
        app.logger.info("Fetching employee")
        app.logger.info(jrows)
        return jrows

@app.route('/employee-summary/', methods=['GET'])
def getEmployeeSummary():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * \
             FROM Employee \
             JOIN Branch ON Branch.BranchID = Employee.BranchID \
             GROUP BY Employee.BranchID"
    cursor.execute(query)
    rows = cursor.fetchall()
    jrows = jsonify(rows)
    app.logger.info(jrows)
    return jrows

@app.route('/employee/<id>', methods=['GET', 'POST', 'DELETE'])
def employeeId(id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'GET':
        # TODO: Modify this to fetch only id
        query = "SELECT * \
                FROM Employee \
                JOIN Branch ON Branch.BranchID = Employee.BranchID \
                WHERE Employee.EmployeeID=%s"
        cursor.execute(query, (id,))
        rows = cursor.fetchall()
        jrows = jsonify(rows)
        app.logger.info(jrows)
        return jrows
    elif request.method == 'POST':
        app.logger.info("Updating Employee")
        data = request.form
        EmployeeID = data["EmployeeID"]
        Name = data["Name"]
        BranchID = data["BranchID"]
        app.logger.info(EmployeeID)
        query = f"SELECT * FROM Employee WHERE EmployeeID = %s"
        cursor.execute(query, (EmployeeID,))
        app.logger.info(query)
        res = cursor.fetchone()
        if res is None:
            query = f"INSERT INTO Employee (EmployeeID, Name, BranchID) VALUES (%s, %s, %s)"
            app.logger.info("query:" + query)
            cursor.execute(query, (EmployeeID, Name, BranchID))
            connection.commit()
            ret = cursor.fetchall()
            return jsonify(ret)
        else:
            query = f"UPDATE Employee SET Name = %s, BranchID = %s WHERE EmployeeID = %s"
            app.logger.info("query:" + query)
            cursor.execute(query, (Name, BranchID, EmployeeID))
            connection.commit()
            return cursor.rowcount

    elif request.method == 'DELETE':
        data = request.form
        EmployeeID = data["EmployeeID"]
        query = f"DELETE FROM Employee WHERE EmployeeID = %s"
        app.logger.info("query:" + query)
        try:
            cursor.execute(query, (EmployeeID,))
            connection.commit()
            ret = cursor.fetchall()
            return jsonify(ret)
        except get_mysql_exception:
            return "Unable to delete. (Probably due to deleting an entry where a foreign key is needed.)"

@app.route('/customer', methods=['GET'])
def get_customers():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Customer")
        rows = cursor.fetchall()
        jrows = jsonify(rows)
        app.logger.info("Fetching customer")
        app.logger.info(jrows)
        return jrows

@app.route('/customer-summary/', methods=['GET'])
def getCustomerSummary():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * \
             FROM Customer \
             JOIN `Order` ON Order.CustomerID = Customer.CustomerID \
             GROUP BY Customer.CustomerID"
    cursor.execute(query)
    rows = cursor.fetchall()
    jrows = jsonify(rows)
    app.logger.info(jrows)
    return jrows

@app.route('/customer/<id>', methods=['GET', 'POST', 'DELETE'])
def customerId(id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'GET':
        # TODO: Modify this to fetch only id
        query = "SELECT * \
                FROM Customer \
                JOIN `Order` ON Order.CustomerID = Customer.CustomerID \
                WHERE Customer.CustomerID=%s"
        cursor.execute(query, (id,))
        rows = cursor.fetchall()
        jrows = jsonify(rows)
        app.logger.info(jrows)
        return jrows
    elif request.method == 'POST':
        app.logger.info("Updating Customer")
        data = request.form
        CustomerID = data["CustomerID"]
        Name = data["Name"]
        Email = data["Email"]
        Phone = data["Phone"]
        app.logger.info(CustomerID)
        query = f"SELECT * FROM Customer WHERE CustomerID = %s"
        cursor.execute(query, (CustomerID,))
        app.logger.info(query)
        res = cursor.fetchone()
        if res is None:
            query = f"INSERT INTO Customer (CustomerID, Name, Email, Phone) VALUES (%s, %s, %s, %s)"
            app.logger.info("query:" + query)
            cursor.execute(query, (CustomerID, Name, Email, Phone))
            connection.commit()
            ret = cursor.fetchall()
            return jsonify(ret)
        else:
            query = f"UPDATE Customer SET Name = %s, Email = %s, Phone = %s WHERE CustomerID = %s"
            app.logger.info("query:" + query)
            cursor.execute(query, (Name, Email, Phone, CustomerID))
            connection.commit()
            return cursor.rowcount

    elif request.method == 'DELETE':
        data = request.form
        CustomerID = data["CustomerID"]
        query = f"DELETE FROM Customer WHERE CustomerID = %s"
        app.logger.info("query:" + query)
        try:
            cursor.execute(query, (CustomerID,))
            connection.commit()
            ret = cursor.fetchall()
            return jsonify(ret)
        except get_mysql_exception:
            return "Unable to delete. (Probably due to deleting an entry where a foreign key is needed.)"

@app.route('/order', methods=['GET'])
def get_orders():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'GET':
        cursor.execute("SELECT * FROM `Order`")
        rows = cursor.fetchall()
        jrows = jsonify(rows)
        app.logger.info("Fetching order")
        app.logger.info(jrows)
        return jrows

@app.route('/order-summary/', methods=['GET'])
def getOrderSummary():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * \
             FROM Customer \
             JOIN `Order` ON Order.CustomerID = Customer.CustomerID \
             GROUP BY Order.OrderID"
    cursor.execute(query)
    rows = cursor.fetchall()
    jrows = jsonify(rows)
    app.logger.info(jrows)
    return jrows

@app.route('/order/<id>', methods=['GET', 'POST', 'DELETE'])
def orderId(id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'GET':
        # TODO: Modify this to fetch only id
        query = "SELECT * \
                FROM `Order` \
                JOIN Customer ON Order.CustomerID = Customer.CustomerID \
                JOIN Employee ON Order.EmployeeID = Employee.EmployeeID \
                JOIN Product ON Order.ProductID = Product.ProductID \
                WHERE Order.OrderID=%s"
        cursor.execute(query, (id,))
        rows = cursor.fetchall()
        jrows = jsonify(rows)
        app.logger.info(jrows)
        return jrows
    elif request.method == 'POST':
        app.logger.info("Updating Order")
        data = request.form
        OrderID = data["OrderID"]
        OrderDate = convertTime(data["OrderDate"])
        app.logger.info(OrderDate)
        CustomerID = data["CustomerID"]
        EmployeeID = data["EmployeeID"]
        ProductID = data["ProductID"]
        Quantity = data["Quantity"]
        app.logger.info(OrderID)
        query = f"SELECT * FROM `Order` WHERE OrderID = %s"
        cursor.execute(query, (OrderID,))
        app.logger.info(query)
        res = cursor.fetchone()
        cursor.execute("SET SQL_MODE='ALLOW_INVALID_DATES'")
        if res is None:
            query = f"INSERT INTO `Order` (OrderID, OrderDate, CustomerID, EmployeeID, ProductID, Quantity) VALUES (%s, %s, %s, %s, %s, %s)"
            app.logger.info("query:" + query)
            cursor.execute(query, (OrderID, OrderDate, CustomerID, EmployeeID, ProductID, Quantity))
            connection.commit()
            ret = cursor.fetchall()
            return jsonify(ret)
        else:
            query = f"UPDATE `Order` SET OrderDate = %s, CustomerID = %s, EmployeeID = %s, ProductID = %s, Quantity = %s WHERE OrderID = %s"
            app.logger.info("query:" + query)
            cursor.execute(query, (OrderDate, CustomerID, EmployeeID, ProductID, Quantity, OrderID))
            connection.commit()
            return cursor.rowcount

    elif request.method == 'DELETE':
        data = request.form
        OrderID = data["OrderID"]
        query = f"DELETE FROM `Order` WHERE OrderID = %s"
        app.logger.info("query:" + query)
        try:
            cursor.execute(query, (OrderID,))
            connection.commit()
            ret = cursor.fetchall()
            return jsonify(ret)
        except get_mysql_exception:
            return "Unable to delete. (Probably due to deleting an entry where a foreign key is needed.)"

@app.route('/shipping', methods=['GET'])
def get_shippings():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Shipping")
        rows = cursor.fetchall()
        jrows = jsonify(rows)
        app.logger.info("Fetching shipping")
        app.logger.info(jrows)
        return jrows

@app.route('/shipping-summary/', methods=['GET'])
def getShippingSummary():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    #query = "SELECT * \
    #         FROM Shipping \
    #         JOIN `Order` ON Order.ShippingID = Shipping.ShippingID \
    #         GROUP BY Shipping.ShippingID"
    query = "SELECT * FROM Shipping"
    cursor.execute(query)
    rows = cursor.fetchall()
    jrows = jsonify(rows)
    app.logger.info(jrows)
    return jrows

@app.route('/shipping/<id>', methods=['GET', 'POST', 'DELETE'])
def shippingId(id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'GET':
        # TODO: Modify this to fetch only id
        #query = "SELECT * \
        #        FROM Shipping \
        #        JOIN `Order` ON Order.ShippingID = Shpping.ShippingID \
        #        WHERE Shipping.ShippingID=%s"
        query = "SELECT * \
                 FROM Shipping \
                 WHERE Shipping.ShippingID =%s"
        cursor.execute(query, (id,))
        rows = cursor.fetchall()
        jrows = jsonify(rows)
        app.logger.info(jrows)
        return jrows
    elif request.method == 'POST':
        app.logger.info("Updating Shipping")
        data = request.form
        ShippingID = data["ShippingID"]
        OrderID = data["OrderID"]
        CarrierName = data["CarrierName"]
        ShipDate = convertTime(data["ShipDate"])
        app.logger.info(ShippingID)
        query = f"SELECT * FROM Shipping WHERE ShippingID = %s"
        cursor.execute(query, (ShippingID,))
        app.logger.info(query)
        res = cursor.fetchone()
        cursor.execute("SET SQL_MODE='ALLOW_INVALID_DATES'")
        if res is None:
            query = f"INSERT INTO Shipping (ShippingID, OrderID, CarrierName, ShipDate) VALUES (%s, %s, %s, %s)"
            app.logger.info("query:" + query)
            cursor.execute(query, (ShippingID, OrderID, CarrierName, ShipDate))
            connection.commit()
            ret = cursor.fetchall()
            return jsonify(ret)
        else:
            query = f"UPDATE Shipping SET OrderID = %s, CarrierName = %s, ShipDate = %s WHERE ShippingID = %s"
            app.logger.info("query:" + query)
            cursor.execute(query, (OrderID, CarrierName, ShipDate, ShippingID))
            connection.commit()
            return cursor.rowcount

    elif request.method == 'DELETE':
        data = request.form
        ShippingID = data["ShippingID"]
        query = f"DELETE FROM Shipping WHERE ShippingID = %s"
        app.logger.info("query:" + query)
        try:
            cursor.execute(query, (ShippingID,))
            connection.commit()
            ret = cursor.fetchall()
            return jsonify(ret)
        except get_mysql_exception:
            return "Unable to delete. (Probably due to deleting an entry where a foreign key is needed.)"


if __name__ == "__main__":
    app.run(debug=True)
