# Davids Database Shop
A Python/SQL project where admins manage suppliers, products, discounts, and orders, while customers can register, login, check inventory and place orders.

---

## How to Run This Project




### Step 1: Set Up Database Credentials
1. Copy Example_Config.py
2. Rename it to **Config.py**
3. Open Config.py and add your **PostgreSQL credentials**

---

### Step 2: Create the Database and Tables
Before running the program, **copy and paste this SQL script** into your PostgreSQL database:

```sql
-- Create supplier table
CREATE TABLE supplier (
    supplier_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    address TEXT NOT NULL
);

-- Create product table
CREATE TABLE product (
    product_id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    supplier_id INTEGER REFERENCES supplier(supplier_id) ON DELETE SET NULL
);

-- Create customer table
CREATE TABLE customer (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create discount table
CREATE TABLE discount (
    discount_id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    percentage DECIMAL(5,2) NOT NULL CHECK (percentage >= 0 AND percentage <= 100),
    reason TEXT NOT NULL
);

-- Create product_discount table (links products & discounts)
CREATE TABLE product_discount (
    product_id INTEGER REFERENCES product(product_id) ON DELETE CASCADE,
    discount_id INTEGER REFERENCES discount(discount_id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    PRIMARY KEY (product_id, discount_id)
);

-- Create orders table
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customer(customer_id) ON DELETE CASCADE,
    total_price DECIMAL(10,2) NOT NULL CHECK (total_price >= 0),
    order_date TIMESTAMP DEFAULT NOW(),
    confirmed BOOLEAN DEFAULT FALSE
);

-- Create order_item table (products inside an order)
CREATE TABLE order_item (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES product(product_id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL CHECK (quantity > 0)
);

```

### Step 3: Install Required Packages
Run this command in your terminal (example Visual Studio code) to install dependencies:
- pip install psycopg2

### Final Step: Run the Program
Run the following command in your terminal (example Visual Studio code) to start the system:
- python DatabaseShop.py
