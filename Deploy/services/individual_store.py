import pandas as pd
import numpy as np
import cloudpickle

with open("deploy/models/model_lgbm.pkl", "rb") as f:
    lgbm = cloudpickle.load(f)

with open("deploy/models/pipeline.pkl", "rb") as f:
    pipeline = cloudpickle.load(f)

with open("deploy/models/target_encoder.pkl", "rb") as f:
    target_encoder = cloudpickle.load(f)

train_data = pd.read_parquet("deploy/data/train_data.parquet")
deploy_data = pd.read_parquet("deploy/data/deploy_data.parquet")


def transform_predict(data):
    data = data.copy()
    data.loc[:, "Store_id_enc"] = target_encoder.transform(data[["Store_id"]])
    data = pipeline.transform(data)
    return lgbm.predict(data.reshape(1, -1))[0]


def forecast(Store_id, days=60):
    forecast_df = deploy_data[deploy_data["Store_id"] == Store_id]
    train_data_slice = train_data[train_data["Store_id"] == Store_id][["Date",
                                                                       "Sales", "Store_id"]]
    editable_data = forecast_df.copy()
    predictions = []

    for i in range(0, days):
        last_31_data = editable_data.iloc[i:i+31]
        prediction_date = last_31_data.iloc[-1]["Date"]
        prediction = transform_predict(last_31_data)
        predictions.append({
            "Date": prediction_date,
            "Sales": prediction
        })
        editable_data.loc[editable_data["Date"] ==
                          prediction_date, "Sales"] = prediction

    prediction_df = pd.DataFrame(predictions)
    prediction_df["Store_id"] = Store_id
    prediction_df["Type"] = "Forecasted"
    train_data_slice["Type"] = "Current"
    return pd.concat([train_data_slice, prediction_df], axis=0)
