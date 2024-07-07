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

  These can be installed using `pip`:
  ```bash
  pip install Flask jsonify request
  ```

### Database
- The database is based on MySQL.
- Check the status of MySQL by running:
  ```bash
  mysql --version
  ```

## How to Start
1. **use `cd` to enter the folder you want to store this project. If we want to store it in Documents, we should run command `cd Documents`.**

2. **Clone project to local:**
   ```
   git clone https://github.com/marama01/CS338-project.git
   ```
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
   ```bash
   mysql -u root -p --local-infile < sql/load_sample.sql
   ```

5. **Run the Flask Backend:**
   ```bash
   flask --app backend/app run --debug
   ```

6. **Open the Frontend:**
   - Open `index.html` in your web browser to access the application.

## Additional Notes
- Ensure your MySQL server is running before executing the database setup and sample data load commands.
- The `--debug` flag in Flask is optional but recommended during development for better error messages and automatic reloading.

## Current Features
Currently it only supports brand to show, edit, add, delete the brand table in frontend.Also, it supports brand to view all related products and information for a specific brand and summarize all related products for all brands in frontend.

