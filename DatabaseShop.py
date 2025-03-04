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

        choice = input("Enter your choice: ")
        if choice == '1':
            add_supplier()
        elif choice == '2':
            add_product()
        elif choice == '3':
            remove_product()
        elif choice == '4':
            list_suppliers_with_products()
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

        if choice == '0':
            break
        else:
            print("Invalid input. Please try again.")

#-----------Admin funtions--------------#


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

    print("Available Suppliers:")
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
    product_id = int(input("Enter the product ID to remove: "))
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

    print("All products:")
    print("Order:")
    print("Supplier ID - Supplier Name - Product - Quantity - Price - Product ID")
    for product in products:
        print(f"{product[0]} - {product[1]} - {product[2]} - {product[3]} - {product[4]:.2f} - {product[5]}")


# Run the program with function "main()"
main()