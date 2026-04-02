import psycopg2


def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="spy_system",
        user="postgres",
        password="123",
        port="5432"
    )