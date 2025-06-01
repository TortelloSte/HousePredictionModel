from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, confloat, conint
import joblib
import numpy as np
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

MODEL_PATH = "ml/model.pkl"

from pydantic import conint, confloat

class HouseFeatures(BaseModel):
    transaction_date: confloat(gt=1900, lt=2100) = Field(..., example=2013.250)
    house_age: confloat(ge=0, le=100) = Field(..., example=13.5)
    distance_to_mrt: confloat(ge=0, le=100000) = Field(..., example=1500.0)
    number_of_convenience_stores: conint(ge=0, le=50) = Field(..., example=3)
    latitude: confloat(ge=-90, le=90) = Field(..., example=24.982)
    longitude: confloat(ge=-180, le=180) = Field(..., example=121.543)

@app.get("/health") # to check if the api is working
def health_check():
    return {"status": "OK"}

@app.post("/predict") # creation og /predict api on fastapi
def predict_price(features: HouseFeatures):
    if not os.path.exists(MODEL_PATH):
        logger.error("Model file not found")
        raise HTTPException(status_code=500, detail="Model not available")

    try:
        model = joblib.load(MODEL_PATH)
        input_array = np.array([[features.transaction_date,
                                 features.house_age,
                                 features.distance_to_mrt,
                                 features.number_of_convenience_stores,
                                 features.latitude,
                                 features.longitude]])
        prediction = model.predict(input_array)
        predicted_price = prediction[0]
        logger.info(f"Prediction made: {predicted_price}")
        return {"predicted_price": predicted_price}
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")