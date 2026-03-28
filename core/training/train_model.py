import pandas as pd
import joblib
from lightgbm import LGBMClassifier

from core.features.feature_builder import build_features
from core.features.label_builder import create_labels


def load_data():
    df = pd.read_csv("data/spy_1m.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def prepare_dataset(df):
    # build features
    df = build_features(df)

    # create labels (training only)
    df = create_labels(df)

    # remove NaNs from rolling features
    df = df.dropna()

    # feature list (must match inference)
    feature_cols = [
        "return_5",
        "return_15",
        "volatility_30",
        "distance_from_open",
        "drawdown",
        "minute_of_day"
    ]

    X = df[feature_cols]
    y = df["label"]

    return X, y, feature_cols


def train():
    df = load_data()

    X, y, feature_cols = prepare_dataset(df)

    # model
    model = LGBMClassifier()

    model.fit(X, y)

    # save with versioning
    joblib.dump(model, "models/model_v1.joblib")
    joblib.dump(feature_cols, "models/features_v1.joblib")

    print("Model trained and saved successfully")


if __name__ == "__main__":
    train()