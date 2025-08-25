import pandas as pd
import numpy as np
import pickle


def load_model():
    with open(f"deploy/models/prophet_global.pkl", "rb") as f:
        return pickle.load(f)


train_data = pd.read_parquet("deploy/data/train_prophet.parquet")
test_data = pd.read_parquet("deploy/data/test_prophet.parquet")


def forecast(days=60):
    forecast_df = test_data.groupby("ds").sum().reset_index().drop(
        columns=["Region_Code"], axis=1)

    train_data_slice = train_data.groupby(["Date"]).sum().drop(
        "Region_Code", axis=1).reset_index()

    model = load_model()
    prediction_df = model.predict(forecast_df.iloc[:days])
    # prediction_df["Region_Code"] = Region_Code
    prediction_df["Type"] = "Forecasted"
    train_data_slice["Type"] = "Current"
    prediction_df = prediction_df[["ds", "yhat", "Type"]]
    prediction_df = prediction_df.rename(
        columns={"yhat": "Total_Sales", "ds": "Date"})

    return pd.concat([train_data_slice, prediction_df], axis=0)
