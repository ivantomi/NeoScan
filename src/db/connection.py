import psycopg2

conn = psycopg2.connect(
    host="tyke.db.elephantsql.com",
    database="moxpgtli",
    user="moxpgtli",
    password="cKGW7RmJsP6H7SbTOADebBUXMNUpEBvT",
    connect_timeout=8,
)

conn.autocommit = True

try:
    q = """
        CREATE TABLE IF NOT EXISTS users(
            id int PRIMARY KEY,
            order_number SERIAL,
            first_name VARCHAR(80),
            last_name VARCHAR(80),
            email VARCHAR(80),
            title VARCHAR(80),
            arrival VARCHAR(80)
        )
    """
    with conn.cursor() as cursor:
            cursor.execute(q)
except Exception as error:
        print(error)

