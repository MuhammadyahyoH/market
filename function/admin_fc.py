from core.db_settings import execute_query

# 1. Show all products
def show_all_products():
    rows = execute_query(
        "SELECT id, title, price, description FROM products ORDER BY id",
        fetch="all"
    )
    if not rows:
        print("No products available.")
        return
    for row in rows:
        print(f"{row['id']}. {row['title']} - ${row['price']} | {row['description']}")


# 2. Add new product
def add_new_product():
    title = input("Product title: ")
    price = input("Product price: ")
    description = input("Product description: ")

    execute_query(
        "INSERT INTO products (title, price, description) VALUES (%s, %s, %s)",
        (title, price, description)
    )

    print("Product added successfully.")



# 3. Delete product
def delete_product():
    show_all_products()
    product_id = int(input("Enter product ID to delete: "))
    execute_query("DELETE FROM products WHERE id = %s", (product_id,))
    print("Product deleted.")


# 4. Show today's menu
from datetime import date

def show_today_menu():
    today = date.today()
    rows = execute_query(
        """
        SELECT mp.id, p.title AS name, p.price, mp.amount
        FROM menu_products mp
        JOIN products p ON mp.product_id = p.id
        WHERE mp.date_of_menu = %s
        """,
        (today,),
        fetch="all"
    )
    if not rows:
        print("Today's menu is empty.")
        return

    for row in rows:
        print(f"{row['id']}. {row['name']} - ${row['price']} | Amount: {row['amount']}")



# 5. Add product to today's menu
def add_to_today_menu():
    show_all_products()
    product_id = int(input("Enter product ID to add to today's menu: "))
    amount = int(input("Enter amount: "))
    today = date.today()

    # Check if already in menu
    existing = execute_query(
        "SELECT id, amount FROM menu_products WHERE product_id = %s AND date_of_menu = %s",
        (product_id, today),
        fetch="one"
    )

    if existing:
        # Update amount
        execute_query(
            "UPDATE menu_products SET amount = amount + %s WHERE id = %s",
            (amount, existing['id'])
        )
        print("Product amount updated in today's menu.")
    else:
        # Insert new menu entry
        execute_query(
            "INSERT INTO menu_products (date_of_menu, product_id, amount) VALUES (%s, %s, %s)",
            (today, product_id, amount)
        )
        print("Product added to today's menu.")



# 6. Remove product from today's menu
def remove_from_today_menu():
    show_today_menu()
    menu_id = int(input("Enter menu ID to remove: "))
    execute_query(
        "DELETE FROM menu_products WHERE id = %s",
        (menu_id,)
    )
    print("Product removed from today's menu.")


# 7. Show all orders
def show_all_orders():
    rows = execute_query(
        """
        SELECT 
            o.id,
            u.name AS user_name,
            p.title AS product_name,
            mp.amount AS menu_amount,
            o.amount AS order_amount,
            o.status,
            o.order_type,
            o.created_at
        FROM orders o
        JOIN users u ON o.user_id = u.id
        JOIN menu_products mp ON o.menu_product_id = mp.id
        JOIN products p ON mp.product_id = p.id
        ORDER BY o.created_at
        """,
        fetch="all"
    )

    if not rows:
        print("No orders yet.")
        return

    for row in rows:
        status = "Done" if row['status'] else "Pending"
        print(f"Order {row['id']}: {row['user_name']} ordered {row['order_amount']} x {row['product_name']} "
              f"(Menu amount: {row['menu_amount']}) | Type: {row['order_type']} | {status} | {row['created_at']}")


# 8. Change order status
def change_order_status():
    show_all_orders()
    order_id = int(input("Enter order ID to change status: "))
    new_status = input("New status (pending/done/canceled): ")
    execute_query(
        "UPDATE orders SET status = %s WHERE id = %s",
        (new_status, order_id)
    )
    print("Order status updated.")
