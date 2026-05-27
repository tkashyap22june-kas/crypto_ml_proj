from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os

from crypto.utils.main_utils import load_object

app = FastAPI()

MODEL_PATH = os.path.join("artifact", "model_trainer", "model.pkl")

model = None


@app.on_event("startup")
def load_model():
    global model
    try:
        model = load_object(MODEL_PATH)
        print("Model loaded successfully")
    except Exception as e:
        print("Model loading failed:", e)
        model = None


class PredictionInput(BaseModel):
    open: float
    high: float
    low: float
    volume: float
    marketCap: float


@app.get("/")
def home():
    return {"message": "Crypto ML API is running"}


@app.post("/predict")
def predict(data: PredictionInput):
    if model is None:
        return {"error": "Model not loaded"}

    df = pd.DataFrame([[data.open, data.high, data.low, data.volume, data.marketCap]],
                      columns=["open", "high", "low", "volume", "marketCap"])

    pred = model.predict(df)

    return {"prediction": float(pred[0])}
