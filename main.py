from auth.login import login_user, register_user
from function.admin_fc import show_all_products, add_new_product, delete_product, show_today_menu, add_to_today_menu, \
    remove_from_today_menu, show_all_orders, change_order_status
from function.user_fc import show_today_menu_user, place_order, show_my_orders, cancel_order
from utils.menu import auth_menu, user_menu, admin_menu
import asyncio


def admin_panel():
    while True:
        print(admin_menu)
        choice = input("Choose: ")

        if choice == "1":
            show_all_products()
        elif choice == "2":
            add_new_product()
        elif choice == "3":
            delete_product()
        elif choice == "4":
            show_today_menu()
        elif choice == "5":
            add_to_today_menu()
        elif choice == "6":
            remove_from_today_menu()
        elif choice == "7":
            show_all_orders()
        elif choice == "8":
            change_order_status()
        elif choice == "9":
            break
        else:
            print("Invalid choice")


def user_panel(user_id: int):
    while True:
        print(user_menu)
        choice = input("Choose: ")

        if choice == "1":
            show_today_menu_user()
        elif choice == "2":
            place_order(user_id)  # ✅ Pass user_id
        elif choice == "3":
            show_my_orders(user_id)  # ✅ Pass user_id
        elif choice == "4":
            cancel_order(user_id)  # ✅ Pass user_id
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")


async def main():
    while True:
        print(auth_menu)
        choice = input("Choose: ")
        if choice == "1":
            user = login_user()
            if user:
                if user.get("role") == "admin":
                    admin_panel()
                else:
                    user_panel(user["id"])  # Pass user_id!
        elif choice == "2":
            register_user()
        elif choice == "3":
            print("Bye!")
            break


if __name__ == "__main__":
    asyncio.run(main())
