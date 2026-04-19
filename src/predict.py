import joblib
import pandas as pd
from src.preprocessing import preprocess
model = joblib.load("models/noshow_model.pkl")
def predict(df: pd.DataFrame):
    X = preprocess(df)
    probs = model.predict_proba(X)[:, 1]
    return probs
