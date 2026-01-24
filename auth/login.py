from core.db_settings import execute_query
from core.config import ADMIN_PHONE, ADMIN_PASSWORD
import logging

logger = logging.getLogger(__name__)

def register_user():
    print("Register")
    name = input("Name: ")
    phone = input("Phone: ")
    password = input("Password: ")

    user = execute_query(
        "SELECT id FROM users WHERE phone = %s",(phone,), fetch="one"
    )

    if user:
        print("User already exists")
        logger.warning("User exists")
        return None

    execute_query(
        "INSERT INTO users (name, phone, password, role) VALUES (%s, %s, %s, %s)",(name, phone, password, "user")
    )
    print("Registration successful!")
    return True


def login_user():
    print("Login")
    phone = input("Phone: ")
    password = input("Password: ")

    if phone == ADMIN_PHONE and password == ADMIN_PASSWORD:
        print("Welcome Admin")
        return {
            "id": 0,
            "name": "Admin",
            "role": "admin"
        }

    user = execute_query(
        "SELECT * FROM users WHERE phone = %s AND password = %s",(phone, password),fetch="one"
    )

    if not user:
        print("Wrong phone or password")
        logger.warning("Failed login attempt")
        return None

    print(f"Welcome {user['name']} ")
    return user
