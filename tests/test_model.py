import joblib
import os
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pytest

model_path = "ml/model.pkl"

def test_model_loading_and_prediction():
    assert os.path.exists(model_path), "Model file not found"

    model = joblib.load(model_path)

    # Realistic input
    test_input = np.array([[2013.5, 10.0, 300.0, 3, 24.963, 121.540]])
    prediction = model.predict(test_input)

    assert prediction.shape == (1,), "Prediction shape is incorrect"
    assert prediction[0] > 0, "Prediction should be a positive number"

def test_model_is_random_forest():
    model = joblib.load(model_path)
    assert isinstance(model, RandomForestRegressor), "Loaded model is not a RandomForestRegressor"

def test_model_fails_on_wrong_shape():
    model = joblib.load(model_path)
    # Wrong input shape: missing one feature
    invalid_input = np.array([[2013.5, 10.0, 300.0, 3, 24.963]])

    with pytest.raises(ValueError):
        model.predict(invalid_input)

def test_model_handles_extreme_values():
    model = joblib.load(model_path)
    extreme_input = np.array([[3000.0, 100.0, 100000.0, 100, 0.0, 0.0]])

    prediction = model.predict(extreme_input)
    assert prediction.shape == (1,), "Prediction should return one result"
    assert isinstance(prediction[0], float), "Prediction should return a float value"