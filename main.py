from auth.login import login_user, register_user
from utils.menu import auth_menu, admin_menu, user_menu
from core.db_settings import execute_query
from core import models
import asyncio


def create_tables():
    execute_query(models.users_table)
    execute_query(models.products_table)


async def admin_panel():
    while True:
        print(admin_menu)
        choice = input("Choose: ")
        if choice == "1":
            await get_all_products()
        elif choice == "2":
            await add_new_product()
        elif choice == "3":
            await delete_product()
        elif choice == "4":
            await show_todays_menu()
        elif choice == "5":
            await add_product_to_todays_menu()
        elif choice == "6":
            await remove_product_from_todays_menu()
        elif choice == "7":
            await show_orders_by_time()
        elif choice == "8":
            await change_order_status()
        elif choice == "9":
            break
        else:
            print("Invalid choice.")

async def user_panel(user):
    user_id = user['id']
    while True:
        print(user_menu)
        choice = input("Choose: ")
        if choice == "1":
            await show_todays_menu()
        elif choice == "2":
            await place_order(user_id)
        elif choice == "3":
            await show_my_orders(user_id)
        elif choice == "4":
            await cancel_order(user_id)
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


async def main():
    while True:
        print(auth_menu)
        choice = input("Choose: ")
        if choice == "1":
            user = await login_user()  # Must be async
            if user:
                if user.get("role") == "admin":
                    await admin_panel()
                else:
                    await user_panel(user)
        elif choice == "2":
            await register_user()  # Must be async
        elif choice == "3":
            print("Bye!")
            break

if __name__ == "__main__":
    asyncio.run(main())
