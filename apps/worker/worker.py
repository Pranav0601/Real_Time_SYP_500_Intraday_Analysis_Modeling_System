# apps/worker/worker.py

import time
import pandas as pd
import yfinance as yf
import os

from core.models.live_pipeline import run_live_pipeline
from core.db.insert import insert_prediction

# ---------------------------
# CONFIG
# ---------------------------
SYMBOL = "SPY"
INTERVAL = "1m"
FETCH_INTERVAL = 60  # seconds

TIMESTAMP_FILE = "data/last_timestamp.txt"


# ---------------------------
# FETCH DATA
# ---------------------------
def fetch_data():
    df = yf.download(SYMBOL, interval=INTERVAL, period="1d")

    if df.empty:
        raise ValueError("No data fetched")

    df = df.reset_index()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.rename(columns={
        "Datetime": "timestamp",
        "Open": "open_spy",
        "High": "high_spy",
        "Low": "low_spy",
        "Close": "close_spy",
        "Volume": "volume_spy"
    }, inplace=True)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


# ---------------------------
# SAVE TO DB (ONLY)
# ---------------------------
def save_result(result):
    os.makedirs("data", exist_ok=True)

    current_ts = str(result["timestamp"])

    # ---------------------------
    # DUPLICATE CHECK
    # ---------------------------
    if os.path.exists(TIMESTAMP_FILE):
        with open(TIMESTAMP_FILE, "r") as f:
            last_ts = f.read().strip()

        if last_ts == current_ts:
            print("Duplicate timestamp, skipping DB insert")
            return

    # update last timestamp
    with open(TIMESTAMP_FILE, "w") as f:
        f.write(current_ts)

    # ---------------------------
    # INSERT INTO DB
    # ---------------------------
    try:
        insert_prediction(result)
        print("Inserted into DB:", result)
    except Exception as e:
        print("DB insert error:", e)


# ---------------------------
# WORKER LOOP
# ---------------------------
def run_worker():
    print("Worker started...")

    while True:
        try:
            print("Fetching data...")
            df = fetch_data()

            print("Running pipeline...")
            result = run_live_pipeline(df)

            print("Saving to DB...")
            save_result(result)

        except Exception as e:
            print("Worker error:", e)

        time.sleep(FETCH_INTERVAL)


# ---------------------------
# ENTRY
# ---------------------------
if __name__ == "__main__":
    run_worker()