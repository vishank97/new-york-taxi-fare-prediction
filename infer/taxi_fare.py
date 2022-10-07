import mlfoundry as mlf
import pandas as pd

client = mlf.get_client(api_key='djE6dHJ1ZWZvdW5kcnk6dmlzaGFuay1iZXRhdGVzdDoyMzFhYzk=',tracking_uri='https://app.develop.truefoundry.tech')
model_version = client.get_model('model:truefoundry/vishank-betatest/taxi-fare-prediction/xgboost-regressor:1')
model = model_version.load()

def infer_model(pickup_datetime,pickup_latitude,pickup_longitude,dropoff_latitude,dropoff_longitude,passenger_count):
    # map the encoded values here
    to_predict = [pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,passenger_count,pickup_datetime]

    test = pd.DataFrame(data=[to_predict],columns=['pickup_longitude', 'pickup_latitude', 'dropoff_longitude',
    'dropoff_latitude', 'passenger_count','pickup_datetime'
    ])
    test = test.astype({'pickup_datetime':'datetime64'})
    test['month'] = test.pickup_datetime.dt.month
    test['year'] = test.pickup_datetime.dt.year
    test['hour'] = test.pickup_datetime.dt.hour
    test['day_of_week'] = test.pickup_datetime.dt.dayofweek
    test.drop(columns=['pickup_datetime'],inplace=True)
    prediction = model.predict(test)
    return {'Fare':float(prediction[0])}