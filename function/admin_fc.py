from datetime import datetime
from core.db_settings import execute_query
from auth.login import login_user, register_user
from utils.menu import auth_menu, admin_menu, user_menu
from core import models

async def get_all_products() -> list[dict]:
    query = "SELECT id, title, price, description FROM products"
    products = await execute_query(query, fetch="all")
    if not products:
        print("No products found.")
        return []
    print("All Products:")
    for p in products:
        print(f"Id {p['id']} | {p['title']} | Price: {p['price']} | {p['description']}")
    return products

async def add_new_product() -> None:
    title = input("Title: ")
    price = input("Price: ")
    description = input("Description: ")
    query = "INSERT INTO products (title, price, description, created_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)"
    await execute_query(query, (title, price, description))
    print("Product added!")

async def delete_product() -> None:
    products = await get_all_products()
    if not products:
        return
    product_id = input("Enter product ID to delete: ")
    query = "DELETE FROM products WHERE id = %s"
    await execute_query(query, (product_id,))
    print("Product deleted!")

async def show_todays_menu() -> None:
    today = datetime.now().date()
    query = """
        SELECT mp.id, p.title, p.price, mp.amount
        FROM menu_products mp
        JOIN products p ON mp.product_id = p.id
        WHERE DATE(mp.date_of_menu) = %s
    """
    menu = await execute_query(query, (today,), fetch="all")
    if not menu:
        print("Today's menu is empty.")
        return
    print("Today's Menu:")
    for item in menu:
        print(f"Id {item['id']} | {item['title']} | Price: {item['price']} | Amount: {item['amount']}")

async def add_product_to_todays_menu() -> None:
    products = await get_all_products()
    if not products:
        return
    product_id = input("Which product ID to add to today's menu? ")
    amount = input("Number of portions: ")
    date_of_menu = datetime.now().date()
    query = "INSERT INTO menu_products (date_of_menu, product_id, amount, created_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)"
    await execute_query(query, (date_of_menu, product_id, amount))
    print("Added to today's menu!")

async def remove_product_from_todays_menu() -> None:
    today = datetime.now().date()
    query = "SELECT mp.id, p.title FROM menu_products mp JOIN products p ON mp.product_id = p.id WHERE DATE(mp.date_of_menu) = %s"
    menu = await execute_query(query, (today,), fetch="all")
    if not menu:
        print("Today's menu is empty.")
        return
    print("Today's Menu:")
    for item in menu:
        print(f"Id {item['id']} | {item['title']}")
    menu_id = input("Enter menu product ID to remove: ")
    await execute_query("DELETE FROM menu_products WHERE id = %s", (menu_id,))
    print("Removed from today's menu!")

async def show_orders_by_time() -> None:
    query = """
        SELECT o.id, u.name, d.from_time, d.to_time, o.status, o.amount
        FROM orders o
        JOIN users u ON o.user_id = u.id
        JOIN durations d ON o.duration_id = d.id
        ORDER BY d.from_time ASC, o.id ASC
    """
    orders = await execute_query(query, fetch="all")
    if not orders:
        print("No orders found.")
        return
    print(f"{'ID':<5} {'User':<15} {'Time':<20} {'Status':<10} {'Amount':<5}")
    for o in orders:
        timeslot = f"{o['from_time']} - {o['to_time']}"
        print(f"{o['id']:<5} {o['name']:<15} {timeslot:<20} {o['status']:<10} {o['amount']:<5}")

async def change_order_status() -> None:
    await show_orders_by_time()
    order_id = input("Enter order ID to change status: ")
    new_status = input("Enter new status (pending/completed/cancelled): ")
    await execute_query("UPDATE orders SET status=%s WHERE id=%s", (new_status, order_id))
    print("Order status updated!")