from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS
import json
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(filename='record.log', level=logging.DEBUG)

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
    #elif request.method == 'POST':
    #    app.logger.info("Updating Brand")
    #    data = request.form
    #    #app.logger.info(json.dumps(data))
    #    brandName = data["BrandName"]
    #    brandDescription = data["BrandDescription"]
    #    app.logger.info("Adding the following to brand table:")
    #    app.logger.info("BrandName: " + brandName)
    #    app.logger.info("BrandDescription: " + brandDescription)

    #    query = f"INSERT INTO Brand (BrandName, BrandDescription) VALUES ('{brandName}', '{brandDescription}')"
    #    app.logger.info(query)
    #    cursor.execute(query)
    #    return "good"

@app.route('/brand-summary/', methods=['GET'])
def getBrandSummary():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = f"SELECT Brand.BrandName, COUNT(Product.ProductID), AVG(Product.ProductPrice) \
              FROM Brand \
              JOIN Product ON Product.BrandID = Brand.BrandID \
              GROUP BY Brand.BrandID"
    cursor.execute(query)
    rows = cursor.fetchall()
    jrows = jsonify(rows)
    app.logger.info(jrows)
    return jrows

@app.route('/brand/<brand_id>', methods=['GET', 'POST', 'DELETE'])
def brandId(brand_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    #app.logger.info("In /brands/", brand_id)
    if request.method == 'GET':
        # TODO: Modify this to fetch only id
        query = f"SELECT Brand.BrandName, Product.ProductName, Product.ProductPrice \
                  FROM Brand \
                  JOIN Product on Product.BrandID = Brand.BrandID \
                  WHERE Brand.BrandID = {brand_id}"
        cursor.execute(query)
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
            query = f"INSERT INTO Brand (BrandID, BrandName, BrandDescription) VALUES ('{brandID}', '{brandName}', '{brandDescription}')"
            app.logger.info("query:" + query)
            cursor.execute(query)
            connection.commit()
            ret = cursor.fetchall()
            return jsonify(ret)
        else:
            app.logger.info("Updating the following to brand table:")
            app.logger.info("BrandId: " + brandID)
            app.logger.info("BrandName: " + brandName)

            query = f"UPDATE Brand SET BrandName = '{brandName}', BrandDescription = '{brandDescription}' WHERE BrandID = '{brandID}'"
            app.logger.info("query:" + query)
            cursor.execute(query)
            connection.commit()
            return cursor.rowcount

    elif request.method == 'DELETE':
        app.logger.info("Deleting Brand")
        data = request.form
        brandID = data["BrandID"]
        query = f"DELETE FROM Brand WHERE BrandID = '{brandID}'"
        app.logger.info("query:" + query)
        try:
            cursor.execute(query)
            connection.commit()
            ret = cursor.fetchall()
            return jsonify(ret)
        except:
            return "Unable to delete. (Probably due to deleting an entry where a foreign key is needed.)"


@app.route('/product', methods=['GET'])
def get_products():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Product")
    rows = cursor.fetchall()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)

