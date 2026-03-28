import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:

    # ensure correct order
    df = df.sort_values("timestamp").copy()

    # ---------------------------
    # MOMENTUM
    # ---------------------------
    df["return_5"] = df["close_spy"].pct_change(5)
    df["return_15"] = df["close_spy"].pct_change(15)

    # ---------------------------
    # VOLATILITY
    # ---------------------------
    df["volatility_30"] = df["close_spy"].rolling(30).std()

    # ---------------------------
    # DATE GROUPING
    # ---------------------------
    df["date"] = df["timestamp"].dt.date

    # ---------------------------
    # DISTANCE FROM OPEN
    # ---------------------------
    df["open_price"] = df.groupby("date")["open_spy"].transform("first")
    df["distance_from_open"] = df["close_spy"] - df["open_price"]

    # ---------------------------
    # SESSION HIGH & DRAWDOWN
    # ---------------------------
    df["session_high"] = df.groupby("date")["high_spy"].cummax()
    df["drawdown"] = df["close_spy"] - df["session_high"]

    # ---------------------------
    # TIME
    # ---------------------------
    df["minute_of_day"] = df.groupby("date").cumcount()

    return df