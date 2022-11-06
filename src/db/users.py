from src.db.connection import conn
import random


def create_user(first_name, last_name, title, email):
    
    with conn.cursor() as cursor:
        id = random.randint(100000000, 999999999)
        q = """
            INSERT INTO users(id, first_name, last_name, title, email, arrival)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        cursor.execute(q, (id, first_name, last_name, title, email, "NE"))
        
        result = cursor.fetchone()

        return result


def get_users():
 
    with conn.cursor() as cursor:
        q = "SELECT first_name, last_name, title, arrival, email, id FROM users ORDER BY order_number ASC"
        cursor.execute(q)

        result = cursor.fetchall()

        return [
            {
                "first_name": item[0],
                "last_name": item[1],
                "title": item[2],
                "arrival": item[3],
                "email": item[4],
                "user_id": item[5]
            } for item in result
        ]


def get_user_data(data):
     with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE users
            SET arrival = %s
            WHERE id = %s
        """, ("DA", data, ))

        cursor.execute("""
            SELECT first_name, last_name, title, arrival, email FROM users WHERE id = %s
        """, (data, ))

        result = cursor.fetchall()

        return [
        {
            "first_name": item[0],
            "last_name": item[1],
            "title": item[2],
            "email": item[3]
        } for item in result
    ]

def user_data(data):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT first_name, last_name, title, arrival, email, id FROM users WHERE id = %s
            """, (data, ))
        result = cursor.fetchall()

        return [
            {
                "first_name": item[0],
                "last_name": item[1],
                "title": item[2],
                "arrival": item[3],
                "email": item[4],
                "id": item[5]
            } for item in result
        ]

def delete_user(user_id):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id, ))

        return None


def get_last_user_ID():
    with conn.cursor() as cursor:

        q = """
            SELECT id, first_name, last_name, title FROM users WHERE order_number = (SELECT max(order_number) FROM users)
        """

        cursor.execute(q)
        id = cursor.fetchone()

        return id


def update_user(first_name, last_name, title, email, user_id):
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE users 
            SET first_name = %s,
                last_name = %s,
                title = %s,
                email = %s
            WHERE id = %s
        """, (first_name, last_name, title, email, user_id, ))

        return None


def check_arrival(user_id):
    with conn.cursor() as cursor:
        cursor.execute(
            """
                SELECT arrival FROM users WHERE id = %s
            """, (user_id, )
        )

        result = cursor.fetchall()

        return [
            {
                "arrival": item[0]
            } for item in result
        ]

def check_validity(user_id):
    with conn.cursor() as cursor:
        cursor.execute(
            """
                SELECT id FROM users WHERE id = %s
            """, (user_id, )
        )

        result = cursor.fetchall()

        return [
            {
                "id": item[0]
            } for item in result
        ]

def change_status(user_id):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            UPDATE users
            SET arrival = %s
            WHERE id = %s
            """, ("DA", user_id, )
        )

def delete_all_users ():
    with conn.cursor() as cursor:
        cursor.execute(
            """
                DELETE FROM users;
            """
        )