import pandas as pd
from faker import Faker
import random

fake = Faker()

def generate_branches(num_entries):
    data = []
    branch_ids = [str(fake.uuid4()) for _ in range(num_entries)]
    for branch_id in branch_ids:
        data.append({
            'BranchID': branch_id,
            'BranchName': fake.city(),
            'Location': fake.address().replace('\n', ', ')
        })
    return pd.DataFrame(data), branch_ids

def generate_brands(num_entries):
    data = []
    brand_ids = [str(fake.uuid4()) for _ in range(num_entries)]
    for brand_id in brand_ids:
        data.append({
            'BrandID': brand_id,
            'BrandName': fake.company(),
            'BrandDescription': fake.catch_phrase()
        })
    return pd.DataFrame(data), brand_ids

def generate_customers(num_entries):
    data = []
    customer_ids = [str(fake.uuid4()) for _ in range(num_entries)]
    for customer_id in customer_ids:
        data.append({
            'CustomerID': customer_id,
            'Name': fake.name(),
            'Email': fake.email(),
            'Phone': fake.phone_number()
        })
    return pd.DataFrame(data), customer_ids

def generate_employees(num_entries, branch_ids):
    data = []
    employee_ids = [str(fake.uuid4()) for _ in range(num_entries)]
    for employee_id in employee_ids:
        data.append({
            'EmployeeID': employee_id,
            'Name': fake.name(),
            'Branch_ID': random.choice(branch_ids)
        })
    return pd.DataFrame(data), employee_ids

def generate_orders(num_entries, product_ids, customer_ids, employee_ids):
    data = []
    order_ids = [str(fake.uuid4()) for _ in range(num_entries)]
    for order_id in order_ids:
        data.append({
            'OrderNum': order_id,
            'ProductID': random.choice(product_ids),
            'Quantity': random.randint(1, 10),
            'CustomerID': random.choice(customer_ids),
            'OrderDate': fake.date_time_this_year(),
            'EmployeeID': random.choice(employee_ids)
        })
    return pd.DataFrame(data), order_ids

def generate_products(num_entries, brand_ids):
    data = []
    product_ids = [str(fake.uuid4()) for _ in range(num_entries)]
    for product_id in product_ids:
        data.append({
            'ProductID': product_id,
            'ProductName': fake.word(),
            'ProductPrice': round(random.uniform(10.0, 1000.0), 2),
            'BrandID': random.choice(brand_ids)
        })
    return pd.DataFrame(data), product_ids

def generate_shipping(num_entries, order_ids):
    data = []
    for _ in range(num_entries):
        data.append({
            'ShippingID': str(fake.uuid4()),
            'OrderNum': random.choice(order_ids), 
            'CarrierName': fake.company(),
            'ShipDate': fake.date_time_this_year()
        })
    return pd.DataFrame(data)

num_entries = 10000
branches, branch_ids = generate_branches(num_entries)
brands, brand_ids = generate_brands(num_entries)
customers, customer_ids = generate_customers(num_entries)
employees, employee_ids = generate_employees(num_entries, branch_ids)
products, product_ids = generate_products(num_entries, brand_ids)
orders, order_ids = generate_orders(num_entries, product_ids, customer_ids, employee_ids)
shipping = generate_shipping(num_entries, order_ids)

# Save to CSV
branches.to_csv('./prod_branches.csv', index=False)
brands.to_csv('./prod_brands.csv', index=False)
customers.to_csv('./prod_customers.csv', index=False)
employees.to_csv('./prod_employees.csv', index=False)
orders.to_csv('./prod_orders.csv', index=False)
products.to_csv('./prod_products.csv', index=False)
shipping.to_csv('./prod_shipping.csv', index=False)
