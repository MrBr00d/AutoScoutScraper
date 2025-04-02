from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import xgboost as xgb
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import datetime

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify a list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

def scale_encode_predicting(X, xscaler:StandardScaler, enc:OneHotEncoder):
    # y = yscaler.transform(pd.DataFrame(y))

    X_numeric = X[["age", "mileage"]]
    X_numeric[["age", "mileage"]] = xscaler.transform(X_numeric)

    X_cat = X[["make", "model", "fuel_type", "transmission"]]
    X_cat = pd.DataFrame(enc.transform(X_cat)).astype(bool)
    X_combined = X_numeric.join(X_cat)

    return X_combined, xscaler, enc
def load_and_predict(df_prediction:pd.DataFrame):
    df_prediction["age"] = df_prediction["age"].apply(lambda x: (datetime.datetime.now() - datetime.datetime.fromisoformat(x)).days)
    with open("xstandardscaler.pickle", "rb") as f:
        xscaler:StandardScaler = pickle.load(f)
    with open("encoder.pickle", "rb") as f:
        enc:OneHotEncoder = pickle.load(f)
    with open("regressor.pickle", "rb") as f:
        reg:xgb.XGBRegressor = pickle.load(f)
    
    X = df_prediction.copy()
    # y = X.pop("price")

    X,_,_ = scale_encode_predicting(X,xscaler,enc)
    yhat = reg.predict(X)
    return yhat

def reverse_target(yhat):
    with open("ystandardscaler.pickle", "rb") as f:
        yscaler:StandardScaler = pickle.load(f)
    yhat = pd.DataFrame(yhat)
    return yscaler.inverse_transform(yhat)

class PredictionRequest(BaseModel):
    age: str
    mileage: float
    make: str
    model: str
    fuel_type: str
    transmission: str

class PredictionResponse(BaseModel):
    predicted_price: float

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    # Prepare the input data for the model
    df = pd.DataFrame({"make": request.make,"model":request.model,"mileage": request.mileage,"fuel_type": request.fuel_type,
                       "age": request.age,"transmission": request.transmission}, index=[0])

    # Make the prediction
    prediction = load_and_predict(df)
    prediction = reverse_target(prediction)
    # Return the predicted price
    return PredictionResponse(predicted_price=int(prediction[0][0]))

# To run the FastAPI app, use the command: uvicorn your_script_name:app --reload
