import joblib
import pandas as pd

# load correct files
model = joblib.load("models/model_v1.joblib")
feature_cols = joblib.load("models/features_v1.joblib")


def predict_probability(df):
    X = df[feature_cols]
    return model.predict_proba(X)[:, 1]