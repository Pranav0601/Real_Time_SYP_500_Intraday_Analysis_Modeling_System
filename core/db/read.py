from core.db.connection import get_connection


def get_latest_prediction():
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT timestamp, low_so_far, probability
        FROM predictions
        ORDER BY timestamp DESC
        LIMIT 1
    """

    cur.execute(query)
    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return {
            "timestamp": str(row[0]),
            "low_so_far": float(row[1]),
            "probability": float(row[2])
        }

    return None


def get_last_n_predictions(limit: int = 50):
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT timestamp, low_so_far, probability
        FROM predictions
        ORDER BY timestamp DESC
        LIMIT %s
    """

    cur.execute(query, (limit,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    results = []

    for row in rows:
        results.append({
            "timestamp": str(row[0]),
            "low_so_far": float(row[1]),
            "probability": float(row[2])
        })

    return results