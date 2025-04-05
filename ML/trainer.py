import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pickle
import xgboost as xgb
import psycopg2

def get_data():
    host = "192.168.2.30"
    port = "5432"
    database = "airflow"
    user = "airflow"
    password = "password here"
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM car_data;")
    results = cur.fetchall()

    cur.close()
    conn.close()

    df = pd.DataFrame(results, columns=["guid", "price", "make", "model", "mileage", "fuel_type", "age", "transmission"])
    df = df.astype({"guid": "string", "make": "string", "model": "string", "fuel_type": "string", "transmission": "string"})
    df.loc[(df["price"]<100000) & (df["price"] >500)].to_csv("car_data_clean.csv", index=False)

def load_data():
    df = pd.read_csv("car_data_clean.csv")
    df = df.drop("guid", axis=1)
    X = df.copy()
    y = X.pop("price")
    return X,y

def scale_encode_training(X,y, yscaler:StandardScaler, xscaler:StandardScaler, enc:OneHotEncoder):
    y = yscaler.fit_transform(pd.DataFrame(y))

    X_numeric = X[["age", "mileage"]]
    X_numeric[["age", "mileage"]] = xscaler.fit_transform(X_numeric)

    X_cat = X[["make", "model", "fuel_type", "transmission"]]
    X_cat = pd.DataFrame(enc.fit_transform(X_cat)).astype(bool)
    X_combined = X_numeric.join(X_cat)

    return X_combined, y, yscaler, xscaler, enc

def train():
    yscaler = StandardScaler()
    xscaler = StandardScaler()
    enc = OneHotEncoder(sparse_output=False)
    X, y = load_data()
    X,y,yscaler,xscaler,enc = scale_encode_training(X,y,yscaler,xscaler,enc)
    with open('ystandardscaler.pickle', 'wb') as f:
        pickle.dump(yscaler, f)
    with open('xstandardscaler.pickle', 'wb') as f:
        pickle.dump(xscaler, f)
    with open('encoder.pickle', 'wb') as f:
        pickle.dump(enc, f)

    params = {'alpha': 0,
    'lambda': 1,
    'learning_rate': 0.1,
    'max_depth': 6,
    'min_child_weight': 1,
    'n_estimators': 2000,
    'gamma': 0.01}
    reg = xgb.XGBRegressor(**params)
    reg.fit(X, y)
    with open('regressor.pickle', 'wb') as f:
        pickle.dump(reg, f)
    print("Training complete.")

if __name__ == "__main__":
    get_data()
    train()