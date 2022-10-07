
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import mlfoundry as mlf


def startPreProcessing():

    train_df = pd.read_csv('train/train.csv')

    train_df = train_df[train_df.fare_amount > 0]
    train_df = train_df[train_df.passenger_count > 0]
    train_df = train_df.iloc[np.where((train_df.pickup_latitude >= -90) & (train_df.pickup_latitude <= 90))]
    train_df = train_df.iloc[np.where((train_df.dropoff_latitude >= -90) & (train_df.dropoff_latitude <= 90))]
    train_df = train_df.iloc[np.where((train_df.pickup_longitude >= -180) & (train_df.pickup_longitude <= 180))]
    train_df = train_df.iloc[np.where((train_df.dropoff_longitude >= -180) & (train_df.dropoff_longitude <= 180))]

    train_df = train_df.astype({'pickup_datetime':'datetime64'})

    train_df['month'] = train_df.pickup_datetime.dt.month
    train_df['year'] = train_df.pickup_datetime.dt.year
    train_df['hour'] = train_df.pickup_datetime.dt.hour
    train_df['day_of_week_name'] = train_df.pickup_datetime.dt.day_name()
    train_df['day_of_week'] = train_df.pickup_datetime.dt.dayofweek
    return train_df


def trainModelandLogParams(train_df):
    
    le = OrdinalEncoder()
    train_df['month'] = le.fit_transform(train_df[['month']])

    X = train_df.drop(columns=['key','fare_amount','pickup_datetime','day_of_week_name'])
    y = train_df.fare_amount
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)


    xgb = XGBRegressor()
    xgb.fit(X_train,y_train)
    y_pred_test = xgb.predict(X_test)

    client = mlf.get_client(api_key='djE6dHJ1ZWZvdW5kcnk6dmlzaGFuay1iZXRhdGVzdDoyMzFhYzk=',tracking_uri='https://app.develop.truefoundry.tech')
    # run = client.create_run(project_name="taxi-fare-prediction", run_name="xgb-model")
    run = client.get_run("4c589cd1ac5344b8bf2523148dbf3a60")


    run.log_params(xgb.get_xgb_params())
    run.log_metrics({'mse':round(mean_squared_error(y_test, y_pred_test),2),
                    'rmse':round(mean_squared_error(y_test, y_pred_test,squared=False),2)})
    run.log_model(model=xgb,framework='xgboost',name='xgboost-regressor')
    run.end()


if __name__ == '__main__':
    print('Started Preprocessing')
    train_df = startPreProcessing()
    print('Starting Model Training')
    trainModelandLogParams(train_df)