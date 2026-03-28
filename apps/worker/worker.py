# apps/worker/worker.py

import time
import pandas as pd

from core.models.live_pipeline import run_live_pipeline


def run_worker():

    while True:
        try:
            df = pd.read_csv("data/spy_1m.csv")


            df["timestamp"] = pd.to_datetime(df["timestamp"])

            result = run_live_pipeline(df)

            print("Latest Prediction:", result)

        except Exception as e:
            print("Error:", e)

        # run every 60 seconds
        time.sleep(60)


if __name__ == "__main__":
    run_worker()