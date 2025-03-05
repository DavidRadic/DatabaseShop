import psycopg2
import Config  # Imports database

def connect_to_db():
    try:
        connection = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        return connection
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None

connection = connect_to_db()
if connection is None:
    exit()  # Close program if connection fails
cursor = connection.cursor()

#Main function that runs the entire program
def main():
    while True:
        user_type = input("Enter 'admin' or 'customer' or 'exit' to exit: ").lower()
        if user_type == 'exit':
            break
        elif user_type == 'admin':
            admin_menu()
        elif user_type == 'customer':
            customer_menu()
        else:
            print("Invalid input. Please try again.")

#Admin menu with related functionalities
def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. Add a supplier")
        print("2. Add a product")
        print("3. Remove a product")  
        print("4. List suppliers with products")
        print("5. Edit product quantity")
        print("6. Add a discount")
        print("7. Assign a discount to a product")
        print("8. View discount history")
        print("9. Confirm an order")
        print("10. Decline an order")
        print("0. Exit")

        choice = input("\nEnter your choice: ")
        if choice == '1':
            add_supplier()
        elif choice == '2':
            add_product()
        elif choice == '3':
            remove_product()
        elif choice == '4':
            list_suppliers_with_products()
        elif choice == '5':
            edit_product_quantity()
        elif choice == '6':
            add_discount()
        elif choice == '7':
            assign_discount()
        elif choice == '8':
            view_discount_history()
        elif choice == '9':
            confirm_order()
        elif choice == '10':
            decline_order()
        elif choice == '0':
            break
        else:
            print("Invalid input. Please try again.")

        
#Customer menu with related functionalities
def customer_menu():
    while True:
        print("\nCustomer Menu:")
        print("1. Register")
        print("2. Log in")
        print("3. View available products")
        print("4. Add a product to the cart")
        print("5. View cart")
        print("6. Place an order")
        print("7. View orders")
        print("8. Delete an order")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            register_customer()
        elif choice == '2':
            login_customer()
        elif choice == '3':
            view_available_products()
        elif choice == '0':
            break
        else:
            print("Invalid input. Please try again.")

#------------------------------------------------------------Admin functions------------------------------------------------------------#


#Funtion for adding suppliers
def add_supplier():
    name = input("Enter supplier name: ")
    phone_number = input("Enter supplier phone number: ")
    address = input("Enter supplier address: ")

    cursor.execute("INSERT INTO supplier (name, phone_number, address) VALUES (%s, %s, %s)", (name, phone_number, address))
    connection.commit()
    print("Supplier added successfully.")


#Function for adding products
def add_product():
    # Show available suppliers before input
    cursor.execute("SELECT supplier_id, name FROM supplier ORDER BY supplier_id ASC;")
    suppliers = cursor.fetchall()

    if not suppliers:
        print("No suppliers available. Please add a supplier first.")
        return

    print("\nAvailable Suppliers:")
    for supplier in suppliers:
        print(f"ID: {supplier[0]}, Name: {supplier[1]}")

    # Get supplier ID from user
    supplier_id = int(input("\nEnter the supplier ID from the list above: "))

    # Check if supplier exists before proceeding
    cursor.execute("SELECT supplier_id FROM supplier WHERE supplier_id = %s", (supplier_id,))
    if not cursor.fetchone():
        print("Invalid supplier ID. Please try again.")
        return

    # Get product details from user
    code = input("Enter product code: ")
    name = input("Enter product name: ")
    quantity = int(input("Enter product quantity: "))
    price = float(input("Enter product base price: "))

    # Insert product into database
    cursor.execute(
        "INSERT INTO product (supplier_id, code, name, quantity, price) VALUES (%s, %s, %s, %s, %s)",
        (supplier_id, code, name, quantity, price)
    )
    connection.commit()
    print("Product added successfully.")


#Function for removing products
def remove_product():
    # Show available products before input
    cursor.execute("SELECT product_id, name, quantity FROM product ORDER BY product_id ASC;")
    products = cursor.fetchall()

    if not products:
        print("No products available.")
        return

    print("\nAvailable Products to remove:")
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}, Quantity: {product[2]}")

    # Get product ID and quantity to remove
    product_id = int(input("\nEnter the product ID to remove: "))
    quantity_to_remove = int(input("Enter the quantity to remove: "))

    # Get the current quantity of the product
    cursor.execute("SELECT quantity FROM product WHERE product_id = %s", (product_id,))
    result = cursor.fetchone()

    if result is None:
        print("The product does not exist.")
    else:
        current_quantity = result[0]
        if quantity_to_remove > current_quantity:
            print("The requested quantity to remove is greater than the available quantity.")
        else:
            new_quantity = current_quantity - quantity_to_remove
            cursor.execute("UPDATE product SET quantity = %s WHERE product_id = %s", (new_quantity, product_id))
            connection.commit()
            print(f"{quantity_to_remove} units removed successfully.")


#Function for listing suppliers with products, shows quantity of products and prices
def list_suppliers_with_products():
    cursor.execute("""
        SELECT supplier.supplier_id, supplier.name, product.name, product.quantity, product.price, product.product_id
        FROM product
        JOIN supplier ON product.supplier_id = supplier.supplier_id
        ORDER BY supplier.supplier_id ASC, product.product_id ASC;
    """)
    products = cursor.fetchall()

    print("\nAll products:")
    print("Order:")
    print("Supplier ID - Supplier Name - Product - Quantity - Price - Product ID")
    for product in products:
        print(f"{product[0]} - {product[1]} - {product[2]} - {product[3]} - {product[4]:.2f} - {product[5]}")

#Function lets the admin edit the current product quantity
def edit_product_quantity():
    # Show available products before input
    cursor.execute("SELECT product_id, name, quantity FROM product ORDER BY product_id ASC;")
    products = cursor.fetchall()

    if not products:
        print("No products available.")
        return

    print("\nAvailable Products:")
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}, Quantity: {product[2]}")

    # Get product ID and new quantity
    product_id = int(input("Enter product ID: "))
    new_quantity = int(input("Enter new product quantity: "))

    # Update the quantity in the database
    cursor.execute("UPDATE product SET quantity = %s WHERE product_id = %s", (new_quantity, product_id))
    connection.commit()
    print("Product quantity updated successfully.")


#Function so admin can add new discounts
def add_discount():
    discount_id = input("Enter an id for the new discount: ")
    code = input("Enter discount code: ")
    percentage = float(input("Enter discount percentage: "))
    reason = input("Enter discount reason: ")

    cursor.execute("INSERT INTO discount (discount_id, code, percentage, reason) VALUES (%s, %s, %s, %s)", (discount_id, code, percentage, reason))
    connection.commit()
    print("Discount added successfully.")


#Function so admin can assign a specific discount to a specific product
def assign_discount():
    # Show available products before input
    cursor.execute("SELECT product_id, name FROM product ORDER BY product_id ASC;")
    products = cursor.fetchall()

    if not products:
        print("No products available.")
        return

    print("\nAvailable Products:")
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}")

    # Show available discounts before input
    cursor.execute("SELECT discount_id, code, percentage FROM discount ORDER BY discount_id ASC;")
    discounts = cursor.fetchall()

    if not discounts:
        print("No discounts available. Please add a discount first.")
        return

    print("\nAvailable Discounts:")
    for discount in discounts:
        print(f"ID: {discount[0]}, Code: {discount[1]}, Percentage: {discount[2]}%")

    # Get product ID and discount ID
    product_id = int(input("\nEnter the product ID to assign discount: "))
    discount_id = int(input("Enter the discount ID: "))
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    # Assign discount to product
    cursor.execute("INSERT INTO product_discount (product_id, discount_id, start_date, end_date) VALUES (%s, %s, %s, %s)",
                   (product_id, discount_id, start_date, end_date))
    connection.commit()
    print("Discount assigned successfully.")


#Function so admin can check records of past applied discounts
def view_discount_history():
    cursor.execute("""
        SELECT product_discount.start_date, product_discount.end_date, product.name, discount.code, discount.percentage
        FROM product_discount
        JOIN product ON product_discount.product_id = product.product_id
        JOIN discount ON product_discount.discount_id = discount.discount_id
        ORDER BY product_discount.start_date DESC;
    """)
    discount_history = cursor.fetchall()

    if not discount_history:
        print("No discount history found.")
        return

    print("\nDiscount History:")
    for record in discount_history:
        print(f"Start: {record[0]}, End: {record[1]}, Product: {record[2]}, Code: {record[3]}, Discount: {record[4]}%")


#Function to confirm an order
def confirm_order():
    order_id = int(input("Enter the order ID you want to confirm: "))
    
    #Check if the order exists
    cursor.execute("SELECT confirmed FROM orders WHERE order_id = %s", (order_id,))
    result = cursor.fetchone()

    if result is None:
        print("The order does not exist.")
        return

    if result[0]:  #If order is already confirmed
        print("The order is already confirmed.")
        return

    #Update order status to confirmed
    cursor.execute("UPDATE orders SET confirmed = TRUE WHERE order_id = %s", (order_id,))
    connection.commit()
    
    print("Order confirmed successfully.")


#Function to decline an order
def decline_order():
    order_id = int(input("Enter the order ID you want to decline: "))

    #Check if the order exists
    cursor.execute("SELECT confirmed FROM orders WHERE order_id = %s", (order_id,))
    result = cursor.fetchone()

    if result is None:
        print("The order does not exist.")
        return

    if result[0]:  #If order is already confirmed
        print("The order is already confirmed and cannot be declined.")
        return

    #Retrieve products in the order to restore stock
    cursor.execute("SELECT product_id, quantity FROM order_item WHERE order_id = %s", (order_id,))
    order_items = cursor.fetchall()

    for item in order_items:
        cursor.execute("UPDATE product SET quantity = quantity + %s WHERE product_id = %s", (item[1], item[0]))

    #Delete the order and its items
    cursor.execute("DELETE FROM order_item WHERE order_id = %s", (order_id,))
    cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
    connection.commit()

    print("Order declined successfully.")


#------------------------------------------------------------Customer functions------------------------------------------------------------#


#Function to register a new customer
def register_customer():
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    email = input("Enter your email: ")
    address = input("Enter your address: ")
    city = input("Enter your city: ")
    country = input("Enter your country: ")
    phone_number = input("Enter your phone number: ")
    password = input("Enter your password: ")

    cursor.execute("INSERT INTO customer (first_name, last_name, email, address, city, country, phone_number, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (first_name, last_name, email, address, city, country, phone_number, password))
    connection.commit()
    print("Registration successful.")


#Function to log in a customer with email and password
def login_customer():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    cursor.execute("SELECT customer_id, first_name FROM customer WHERE email = %s AND password = %s", (email, password))
    result = cursor.fetchone()

    if result:
        print(f"Welcome, {result[1]}!")
        return result[0]  # Return the customer ID
    else:
        print("Invalid email or password.")
        return None
    
#Lets the cusomers see what products are available
def view_available_products():
    cursor.execute("""
        SELECT supplier.supplier_id, supplier.name, product.product_id, product.name, 
               product.quantity, product.price, 
               COALESCE(discount.percentage, 0) as discount_percentage
        FROM product
        JOIN supplier ON product.supplier_id = supplier.supplier_id
        LEFT JOIN product_discount 
            ON product.product_id = product_discount.product_id 
            AND current_date BETWEEN product_discount.start_date AND product_discount.end_date
        LEFT JOIN discount ON product_discount.discount_id = discount.discount_id
        ORDER BY supplier.supplier_id ASC, product.product_id ASC;
    """)
    products = cursor.fetchall()

    if not products:
        print("No products available.")
        return

    print("\nAvailable Products:")
    print("Supplier ID - Supplier Name - Product ID - Product Name - Quantity - Price - Discount (%)")

    for product in products:
        print(f"{product[0]} - {product[1]} - {product[2]} - {product[3]} - {product[4]} - {product[5]:.2f} - {product[6]}%")


# Run the program with function "main()"
main()