from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os
import importlib.util

app = FastAPI()

MODEL_PATH = os.path.join("artifact", "model_trainer", "model.pkl")


# 🔥 DIRECT FILE LOAD (NO PACKAGE IMPORTS)
UTIL_PATH = os.path.join("src", "crypto", "utils", "main_utils.py")

spec = importlib.util.spec_from_file_location("main_utils", UTIL_PATH)
main_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main_utils)

load_object = main_utils.load_object

model = load_object(MODEL_PATH)


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

    df = pd.DataFrame([[data.open, data.high, data.low, data.volume, data.marketCap]],
                      columns=["open", "high", "low", "volume", "marketCap"])

    pred = model.predict(df)

    return {"prediction": float(pred[0])}
