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
        print("4. List all products")
        print("5. Edit product quantity")
        print("6. Add a discount")
        print("7. Assign a discount to a product")
        print("8. View discount history")
        print("9. Confirm an order")
        print("10. Decline an order")
        print("0. Exit")

        choice = input("Enter your choice: ")
        if choice == '0':
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

# Run the program with function "main()"
main()