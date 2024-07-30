# Project Setup and Deployment Guide

## Preparation

### Frontend
- The frontend is built using HTML, CSS, and JavaScript.

### Backend
- The backend is developed using Flask in Python.
- Ensure Python is installed by checking the version:
  ```bash
  python --version
  ```
  or
  ```bash
  python3 --version
  ```
- Required libraries:
  - Flask
  - jsonify
  - request
  - jq

  These can be installed using `pip` or `brew / apt`:
  ```bash
  pip install Flask jsonify request flask_cors mysql.connector json
  brew install jq
  ```

### Database
- The database is based on MySQL.
- Check the status of MySQL by running:
  ```bash
  mysql --version
  ```

## How to Start (Normal way)
1. **use `cd` to enter the folder you want to store this project. If we want to store it in Documents, we should run command `cd Documents`.**

2. **Clone project to local:**
   ```
   git clone https://github.com/marama01/CS338-project.git
   ```

3. **Configure the information of database user in `app.py` in folder backend**
   ```
   connection = mysql.connector.connect(
               host="localhost",
               user="root",
               password="12345678",
               database="testdb"
           )
   ```
   Only change the user and the password.  
   **Make sure the user has access to all databases.**
3. **This is an optional step, users can first run command `cd CS338-project`, and then generate production data by running**
   ```
   python3 gen_prod_data/gen_prod_data.py
   ```
   **Then users can see all the production data in folder** `gen_prod_data`.


3. **Set up the MySQL Database:**
   ```bash
   mysql -u root -p < sql/setup.sql
   ```
   If your MySQL root user has a password, use:
   ```bash
   mysql -u root -p"yourpassword" < sql/setup.sql
   ```

4. **Load Sample Data:**  
   If users want to use sample data:
   ```bash
   mysql -u root -p"yourpassword" --local-infile < sql/load_sample.sql
   ```
   If users want to use production data:
    ```bash
   mysql -u root -p"yourpassword" --local-infile < sql/load_prod_data.sql
   ```  

5. **Run the Flask Backend:**
   ```bash
   flask --app backend/app run --debug
   ```

6. **Open the Frontend:**
   - Open `index.html` in your web browser to access the application.


## How to Start using script
1. **use `cd` to enter the folder you want to store this project. If we want to store it in Documents, we should run command `cd Documents`.**

2. **Configure `config.json` with MySQL username and password**
   ```
   {
    "username": "root",
    "password": "12345678"
   }
   ```
   **Make sure the user has access to all databases.**

3. **Configure the information of database user in `app.py` in folder backend**
   ```
   connection = mysql.connector.connect(
               host="localhost",
               user="root",
               password="12345678",
               database="testdb"
           )
   ```
   Only change the user and the password.

3. **Execute the script**
   ```bash
   ./setup.sh
   ```

4. **Following the Hints**
   ```
   HINT:
   The correct step is setup DB, generate data, import data, run flask service

   Choose an option:
   1) Set up SQL database
   2) Delete testdb database
   3) Load sample.csv database
   4) Load gen_prod_data.csv database
   5) Regenerate production data
   6) Run Flask service
   7) Exit
   Enter your choice: 
   ```
   For example, if we want to generate production data first, we can just type 5. If we want to run Flask service, we type 6.

## Additional Notes
- Ensure your MySQL server is running before executing the database setup and sample data load commands.
- The `--debug` flag in Flask is optional but recommended during development for better error messages and automatic reloading.

## Current Features
Currently it only supports brand to show, edit, add, delete the brand table in frontend.