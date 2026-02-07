from datetime import datetime
from core.db_settings import execute_query
from auth.login import login_user, register_user
from utils.menu import auth_menu, admin_menu, user_menu
from core import models

async def show_my_orders(user_id) -> None:
    query = """
        SELECT o.id, d.from_time, d.to_time, o.status, o.amount
        FROM orders o
        JOIN durations d ON o.duration_id = d.id
        WHERE o.user_id = %s
        ORDER BY d.from_time ASC
    """
    orders = await execute_query(query, (user_id,), fetch="all")
    if not orders:
        print("You have no orders.")
        return
    print(f"{'ID':<5} {'Time':<20} {'Status':<10} {'Amount':<5}")
    for o in orders:
        timeslot = f"{o['from_time']} - {o['to_time']}"
        print(f"{o['id']:<5} {timeslot:<20} {o['status']:<10} {o['amount']:<5}")

async def place_order(user_id) -> None:
    await show_todays_menu()
    product_id = input("Enter product ID to order: ")
    amount = input("Number of portions: ")
    # For simplicity, select first duration
    durations = await execute_query("SELECT id, from_time, to_time FROM durations", fetch="all")
    if not durations:
        print("No available durations.")
        return
    print("Available durations:")
    for d in durations:
        print(f"Id {d['id']} | {d['from_time']} - {d['to_time']}")
    duration_id = input("Enter duration ID: ")
    await execute_query("INSERT INTO orders (user_id, duration_id, amount, status, created_at) VALUES (%s, %s, %s, 'pending', CURRENT_TIMESTAMP)",
                        (user_id, duration_id, amount))
    print("Order placed!")

async def cancel_order(user_id) -> None:
    await show_my_orders(user_id)
    order_id = input("Enter order ID to cancel: ")
    await execute_query("UPDATE orders SET status='cancelled' WHERE id=%s AND user_id=%s", (order_id, user_id))
    print("Order cancelled!")