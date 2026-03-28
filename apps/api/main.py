from fastapi import FastAPI
import pandas as pd
import yfinance as yf

from core.models.live_pipeline import run_live_pipeline
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/predict")
def predict():
    try:
        # ---------------------------
        # FETCH LIVE DATA
        # ---------------------------
        df = yf.download("SPY", interval="1m", period="1d")

        if df.empty:
            return {"error": "No data fetched"}

        df = df.reset_index()

        # ---------------------------
        # FLATTEN COLUMNS (IMPORTANT FIX)
        # ---------------------------
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # ---------------------------
        # NOW RENAME
        # ---------------------------
        df.rename(columns={
            "Datetime": "timestamp",
            "Open": "open_spy",
            "High": "high_spy",
            "Low": "low_spy",
            "Close": "close_spy",
            "Volume": "volume_spy"
        }, inplace=True)

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        # ---------------------------
        # RUN PIPELINE
        # ---------------------------
        result = run_live_pipeline(df)
        # ---------------------------
        # ADD STALENESS CHECK
        # ---------------------------
        latest_time = df["timestamp"].iloc[-1]
        now = datetime.now(timezone.utc)

        minutes_diff = (now - latest_time).total_seconds() / 60

        result["minutes_since_last_update"] = round(minutes_diff, 2)

        if minutes_diff > 5:
            result["status"] = "MARKET_CLOSED_OR_STALE"
        else:
            result["status"] = "LIVE"
        return result

    except Exception as e:
        return {"error": str(e)}