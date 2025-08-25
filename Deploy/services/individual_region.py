import pandas as pd
import numpy as np
import pickle


def load_model(Region_Code):
    with open(f"deploy/models/prophet_{Region_Code}.pkl", "rb") as f:
        return pickle.load(f)


train_data = pd.read_parquet("deploy/data/train_prophet.parquet")
test_data = pd.read_parquet("deploy/data/test_prophet.parquet")


def forecast(Region_Code, days=60):
    forecast_df = test_data[test_data["Region_Code"]
                            == Region_Code].drop("Region_Code", axis=1)

    train_data_slice = train_data[train_data["Region_Code"] == Region_Code].groupby(
        ["Date"]).sum().reset_index().drop("Region_Code", axis=1)

    model = load_model(Region_Code)
    prediction_df = model.predict(forecast_df)
    # prediction_df["Region_Code"] = Region_Code
    prediction_df["Type"] = "Forecasted"
    train_data_slice["Type"] = "Current"
    prediction_df = prediction_df[["ds", "yhat", "Type"]]
    prediction_df = prediction_df.rename(
        columns={"yhat": "Total_Sales", "ds": "Date"})

    return pd.concat([train_data_slice, prediction_df], axis=0)
