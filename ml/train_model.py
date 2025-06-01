import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import os
import logging
from datetime import datetime
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_PATH = "data/Real estate.csv"
MODEL_DIR = "ml"
LATEST_MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [col.strip().replace(' ', '_').replace('(', '').replace(')', '') for col in df.columns]
    return df

def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        logger.error(f"Dataset not found: {path}")
        raise FileNotFoundError(f"Dataset not found at {path}")
    logger.info(f"dataset taken from {path}")
    df = pd.read_csv(path)
    return clean_column_names(df)

def train_model(X, y):
    logger.info("start training...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    logger.info("Model TRAINED")
    return model

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    logger.info(f"MSE on test set: {mse:.2f}")

def save_model(model):
    os.makedirs(MODEL_DIR, exist_ok=True)
    date_str = datetime.today().strftime('%Y%m%d')
    versioned_filename = f"model_v{date_str}.pkl"
    versioned_path = os.path.join(MODEL_DIR, versioned_filename)

    # to save the model with the versioning
    joblib.dump(model, versioned_path)
    logger.info(f"model saved as: {versioned_path}")

    # update the model
    shutil.copy(versioned_path, LATEST_MODEL_PATH)
    logger.info(f"last upadte model saved: {LATEST_MODEL_PATH}")

def main():
    df = load_data(DATA_PATH)

    features = ['X1_transaction_date', 'X2_house_age',
                'X3_distance_to_the_nearest_MRT_station',
                'X4_number_of_convenience_stores',
                'X5_latitude', 'X6_longitude']
    target = 'Y_house_price_of_unit_area' # since there is the y in the dataset i use this field as target

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # use all function create in the main one, so we can train, evaluate and save the model here
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)
    save_model(model)

if __name__ == "__main__":
    main() # train the model