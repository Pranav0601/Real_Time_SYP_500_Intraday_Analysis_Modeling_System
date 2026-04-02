from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone

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