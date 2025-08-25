import numpy as np
import pandas as pd


def smape(A, F):
    tmp = 2 * np.abs(F - A) / (np.abs(A) + np.abs(F))
    len_ = np.count_nonzero(~np.isnan(tmp))
    if len_ == 0 and np.nansum(tmp) == 0:  # Deals with a special case
        return 100
    return 100 / len_ * np.nansum(tmp)


def generate_features(result):
    # # Register the resultFrame as a temporary table
    # db.sql(f"CREATE OR REPLACE TEMPORARY TABLE {table_name} AS SELECT * FROM result")

    # query = f"""
    # SELECT *,
    #     lag(Sales, 1) over (partition by Store_id order by Date) as Sales_Lag_1,
    #     lag(Sales, 7) over (partition by Store_id order by Date) as Sales_Lag_7,
    #     lag(Sales, 12) over (partition by Store_id order by Date) as Sales_Lag_12,
    #     lag(Sales, 30) over (partition by Store_id order by Date) as Sales_Lag_30,
    #     avg(Sales) over (partition by Store_id order by Date rows between 7 preceding and 1 preceding) as Sales_Mean_7,
    #     avg(Sales) over (partition by Store_id order by Date rows between 12 preceding and 1 preceding) as Sales_Mean_12,
    #     avg(Sales) over (partition by Store_id order by Date rows between 30 preceding and 1 preceding) as Sales_Mean_30,
    #     stddev_pop(Sales) over (partition by Store_id order by Date rows between 7 preceding and 1 preceding) as Sales_Std_7,
    #     stddev_pop(Sales) over (partition by Store_id order by Date rows between 12 preceding and 1 preceding) as Sales_Std_12,
    #     stddev_pop(Sales) over (partition by Store_id order by Date rows between 30 preceding and 1 preceding) as Sales_Std_30,
    #     avg(Sales) over (partition by Store_id order by Date rows between unbounded preceding and 1 preceding) as Sales_Expanding_Mean,
    #     stddev_pop(Sales) over (partition by Store_id order by Date rows between unbounded preceding and 1 preceding) as Sales_Expanding_Std,
    #     sum(Sales) over (partition by Store_id order by Date rows between unbounded preceding and 1 preceding) as Sales_Expanding_Sum,
    #     --min(Sales) over (partition by Store_id order by Date rows between unbounded preceding and 1 preceding) as Sales_Expanding_Min,
    # from {table_name}
    # """

    # result = db.sql(query).df()

    result = result.sort_values(by=['Store_id', 'Date'])

    # Create lag features
    result['Sales_Lag_1'] = result.groupby('Store_id')['Sales'].shift(1)
    result['Sales_Lag_7'] = result.groupby('Store_id')['Sales'].shift(7)
    result['Sales_Lag_12'] = result.groupby('Store_id')['Sales'].shift(12)
    result['Sales_Lag_30'] = result.groupby('Store_id')['Sales'].shift(30)

    # Create moving average features
    result['Sales_Mean_7'] = result.groupby(
        'Store_id')['Sales'].shift(1).rolling(window=7).mean()
    result['Sales_Mean_12'] = result.groupby(
        'Store_id')['Sales'].shift(1).rolling(window=12).mean()
    result['Sales_Mean_30'] = result.groupby(
        'Store_id')['Sales'].shift(1).rolling(window=30).mean()

    # result['Sales_EMA_7'] = result.groupby('Store_id')['Sales'].shift(1).ewm(span=7, adjust=False).mean()
    # result['Sales_EMA_12'] = result.groupby('Store_id')['Sales'].shift(1).ewm(span=12, adjust=False).mean()
    # result['Sales_EMA_30'] = result.groupby('Store_id')['Sales'].shift(1).ewm(span=30, adjust=False).mean()

    # Create moving standard deviation features
    result['Sales_Std_7'] = result.groupby(
        'Store_id')['Sales'].shift(1).rolling(window=7).std()
    result['Sales_Std_12'] = result.groupby(
        'Store_id')['Sales'].shift(1).rolling(window=12).std()
    result['Sales_Std_30'] = result.groupby(
        'Store_id')['Sales'].shift(1).rolling(window=30).std()

    # create moving min and max features
    result['Sales_Min_7'] = result.groupby(
        'Store_id')['Sales'].shift(1).rolling(window=7).min()
    result['Sales_Min_12'] = result.groupby(
        'Store_id')['Sales'].shift(1).rolling(window=12).min()
    result['Sales_Min_30'] = result.groupby(
        'Store_id')['Sales'].shift(1).rolling(window=30).min()

    result['Sales_Max_7'] = result.groupby(
        'Store_id')['Sales'].shift(1).rolling(window=7).max()
    result['Sales_Max_12'] = result.groupby(
        'Store_id')['Sales'].shift(1).rolling(window=12).max()
    result['Sales_Max_30'] = result.groupby(
        'Store_id')['Sales'].shift(1).rolling(window=30).max()

    # Create expanding mean and standard deviation features
    result['Sales_Expanding_Mean'] = result.groupby(
        'Store_id')['Sales'].shift(1).ewm(alpha=0.9, adjust=False).mean()
    # result['Sales_Expanding_Weighted_Mean'] = result.groupby('Store_id')['Sales'].expanding().apply(lambda x: np.average(x, weights=np.arange(1, len(x)+1))).shift(1).reset_index(level=0, drop=True)
    result['Sales_Expanding_Std'] = result.groupby(
        'Store_id')['Sales'].shift(1).ewm(alpha=0.9, adjust=False).std()
    result['Sales_Expanding_Sum'] = result.groupby(
        'Store_id')['Sales'].expanding().sum().shift(1).reset_index(level=0, drop=True)

    result = result.drop(columns=["Date", "Store_id"], axis=1)
    # encode cyclical features
    result['Day_sin'] = np.sin(2 * np.pi * result['Day']/31)
    result['Day_cos'] = np.cos(2 * np.pi * result['Day']/31)

    result['Day_of_Week_sin'] = np.sin(2 * np.pi * result['Day_of_Week']/6)
    result['Day_of_Week_cos'] = np.cos(2 * np.pi * result['Day_of_Week']/6)

    result['Month_sin'] = np.sin(2 * np.pi * result['Month']/12)
    result['Month_cos'] = np.cos(2 * np.pi * result['Month']/12)

    result['Quarter_sin'] = np.sin(2 * np.pi * result['Quarter']/4)
    result['Quarter_cos'] = np.cos(2 * np.pi * result['Quarter']/4)

    result['Week_sin'] = np.sin(2 * np.pi * result['Week']/52)
    result['Week_cos'] = np.cos(2 * np.pi * result['Week']/52)

    result['Week_of_Month_sin'] = np.sin(2 * np.pi * result['Week_of_Month']/5)
    result['Week_of_Month_cos'] = np.cos(2 * np.pi * result['Week_of_Month']/5)

    # add fourier features for 7 days, 12 days, 30 days
    # result['Day_7_sin'] = np.sin(2 * np.pi * result['Day']/7)
    # result['Day_7_cos'] = np.cos(2 * np.pi * result['Day']/7)

    # result['Day_12_sin'] = np.sin(2 * np.pi * result['Day']/12)
    # result['Day_12_cos'] = np.cos(2 * np.pi * result['Day']/12)

    # drop original cyclical features
    result = result.drop(columns=[
                         'Day', 'Day_of_Week', 'Month', 'Quarter', 'Week', 'Week_of_Month'], axis=1)
    result = result.dropna()

    return result
