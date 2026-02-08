from core.db_settings import execute_query
from datetime import date


def show_today_menu_user():
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
        print(f"{row['id']}. {row['name']} - ${row['price']} | Available: {row['amount']}")


def place_order(user_id: int):
    show_today_menu_user()
    menu_id = int(input("Enter menu ID to order: "))
    amount = int(input("Enter quantity: "))


    duration_id = None
    duration_rows = execute_query("SELECT id, from_time, to_time, seats FROM durations", fetch="all")
    if duration_rows:
        print("Available durations:")
        for d in duration_rows:
            print(f"{d['id']}: {d['from_time']} - {d['to_time']} | Seats: {d['seats']}")
        duration_id = int(input("Enter duration ID: "))

    order_type = input("Enter order type (e.g., dine-in, take-away): ")

    execute_query(
        """
        INSERT INTO orders (user_id, menu_product_id, amount, duration_id, order_type)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (user_id, menu_id, amount, duration_id, order_type)
    )
    print("Order placed successfully!")




def show_my_orders(user_id: int):
    rows = execute_query(
        """
        SELECT o.id, p.title AS product_name, o.amount, o.status, o.order_type, o.created_at
        FROM orders o
        JOIN menu_products mp ON o.menu_product_id = mp.id
        JOIN products p ON mp.product_id = p.id
        WHERE o.user_id = %s
        ORDER BY o.created_at
        """,
        (user_id,),
        fetch="all"
    )

    if not rows:
        print("You have no orders.")
        return

    for row in rows:
        status = "Done" if row['status'] else "Pending"
        print(f"Order {row['id']}: {row['amount']} x {row['product_name']} | {row['order_type']} | {status} | {row['created_at']}")



def cancel_order(user_id: int):
    show_my_orders(user_id)
    order_id = int(input("Enter order ID to cancel: "))
    execute_query(
        "DELETE FROM orders WHERE id = %s AND user_id = %s",
        (order_id, user_id)
    )
    print("Order canceled.")
