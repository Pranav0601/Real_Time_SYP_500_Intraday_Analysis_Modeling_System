import pandas as pd

from core.features.feature_builder import build_features
from core.models.predict import predict_probability


def run_live_pipeline(df: pd.DataFrame):

    # build features
    df = build_features(df)

    # compute low_so_far WITHOUT future leakage
    df["low_so_far"] = df.groupby(df["timestamp"].dt.date)["low_spy"].cummin()

    # remove NaNs from rolling + pct_change
    df = df.dropna()

    if len(df) == 0:
        raise ValueError("No valid rows after feature engineering")

    # prediction
    df["probability"] = predict_probability(df)

    latest = df.iloc[-1]

    return {
        "timestamp": str(latest["timestamp"]),
        "low_so_far": float(latest["low_so_far"]),
        "probability": float(latest["probability"])
    }