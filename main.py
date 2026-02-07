from auth.login import login_user, register_user
from utils.menu import auth_menu, user_menu, admin_menu
import asyncio


def admin_panel():
    while True:
        print(admin_menu)
        choice = input("Choose: ")

        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            pass
        elif choice == "6":
            pass
        elif choice == "7":
            pass
        elif choice == "8":
            pass
        elif choice == "9":
            break
        else:
            print("Invalid choice")


def user_panel():
    while True:
        print(user_menu)
        choice = input("Choose: ")

        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            break
        else:
            print("Invalid choice")



async def main():
    while True:
        print(auth_menu)
        choice = input("Choose: ")
        if choice == "1":
            user =  login_user()
            if user:
                if user.get("role") == "admin":
                   admin_panel()
                else:
                     user_panel()
        elif choice == "2":
             register_user()
        elif choice == "3":
            print("Bye!")
            break

if __name__ == "__main__":
    asyncio.run(main())
