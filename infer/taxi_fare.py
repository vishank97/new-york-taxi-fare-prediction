import mlfoundry as mlf
import pandas as pd
import yaml

with open("infer/infer.yaml", "r") as stream:
    try:
        env_vars = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# Load the model from MLFoundry by proving the MODEL_FQN
client = mlf.get_client(api_key=env_vars['components'][0]['env']['MLF_API_KEY'],tracking_uri=env_vars['components'][0]['env']['MLF_HOST'])
model_version = client.get_model(env_vars['components'][0]['env']['MODEL_FQN'])
model = model_version.load()

def infer_model(pickup_datetime,pickup_latitude,pickup_longitude,dropoff_latitude,dropoff_longitude,passenger_count):
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