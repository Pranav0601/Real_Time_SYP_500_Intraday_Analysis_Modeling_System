from core.db.connection import get_connection


def insert_prediction(result):
    conn = get_connection()
    cur = conn.cursor()

    query = """
        INSERT INTO predictions (timestamp, low_so_far, probability)
        VALUES (%s, %s, %s)
    """

    cur.execute(query, (
        result["timestamp"],
        result["low_so_far"],
        result["probability"]
    ))

    conn.commit()

    cur.close()
    conn.close()