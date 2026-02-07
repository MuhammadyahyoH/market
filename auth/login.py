from core.db_settings import execute_query
from core.config import ADMIN_USERNAME, ADMIN_PASSWORD

def register_user():
    print("=== REGISTER ===")
    name = input("Name: ")
    password = input("Password: ")

    user = execute_query(
        "SELECT id FROM users WHERE name=%s",
        (name,),
        fetch="one"
    )

    if user:
        print("User already exists")
    else:
        execute_query(
            "INSERT INTO users (name, password) VALUES (%s, %s)",
            (name, password)
        )
        print("Registration successful!")


def login_user():
    print("=== LOGIN ===")
    name = input("Name: ")
    password = input("Password: ")

    if name == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Welcome [ADMIN]")
        return {"role": "admin"}

    user = execute_query(
        "SELECT * FROM users WHERE name=%s AND password=%s",
        (name, password),
        fetch="one"
    )

    if not user:
        print("Make sure you are logged in")
        return None

    print(f"Welcome {user['name']}")
    return {"role": "user", "id": user["id"]}
