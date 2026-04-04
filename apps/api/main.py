from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import pandas as pd
import yfinance as yf

from core.db.read import get_latest_prediction, get_last_n_predictions

app = FastAPI()


# ---------------------------
# CORS
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------
# HEALTH
# ---------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------------------
# PREDICT (FROM DB)
# ---------------------------
@app.get("/predict")
def predict():
    try:
        result = get_latest_prediction()

        if not result:
            return {"error": "No data in database yet"}

        latest_time = datetime.fromisoformat(result["timestamp"]).replace(tzinfo=timezone.utc)
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


@app.get("/history")
def history(limit: int = 50):
    try:
        data = get_last_n_predictions(limit)

        if not data:
            return {"error": "No history available"}

        return {
            "count": len(data),
            "data": data
        }

    except Exception as e:
        return {"error": str(e)}
    
# ---------------------------
# NEW: MARKET DATA ENDPOINT
# ---------------------------
@app.get("/market")
def market():
    try:
        df = yf.download("SPY", interval="1m", period="1d")
        if df.empty:
            return {"error": "No market data"}

        df = df.reset_index()

        # flatten columns if needed
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df.rename(columns={
            "Datetime": "timestamp",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        }, inplace=True)

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        # return last ~200 points
        df = df.tail(200)

        return {
            "data": [
                {
                    "timestamp": str(row["timestamp"]),
                    "close": float(row["close"])
                }
                for _, row in df.iterrows()
            ]
        }

    except Exception as e:
        return {"error": str(e)}