import pandas as pd


def create_labels(df: pd.DataFrame) -> pd.DataFrame:

    df["date"] = df["timestamp"].dt.date

    labeled_dfs = []

    for date, group in df.groupby("date"):

        group = group.sort_values("timestamp").copy()

        day_low = group["low_spy"].min()

        group["low_so_far"] = group["low_spy"].cummin()

        group["label"] = (group["low_so_far"] == day_low).astype(int)

        labeled_dfs.append(group)

    result = pd.concat(labeled_dfs)

    return result