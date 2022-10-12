from operator import concat
import streamlit as st
import requests
import yaml
with open("demo/demo.yaml", "r") as stream:
    try:
        env_vars = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}


def main():
    request_url = env_vars['components'][0]['env']['INFER_URL']
    st.set_page_config(page_title="Taxi Fare", page_icon="🚕")
    # with open('demo/taxi.jpg','r') as image:
    st.image('image/taxi.jpg')
    st.title("Taxi Fare Prediction")
    st.header('Welcome to Predict of New York Taxi Fares!')
    st.write('This is a sample app that demonstrates the prowess of ServiceFoundry ML model deployment.🚀')
    st.write('Visit the [Github](https://github.com/vishank97/new-york-taxi-fare-prediction) repo for detailed exaplaination or [Google Colab](https://colab.research.google.com/drive/1WL8cnVmqsWxh9Ok-Ml5axAuxGfnZ1A9S#scrollTo=KDVXAdh7yKei) notebook to get started right away')
    with st.form("my_form"):
        
        pickup_datetime = st.text_input('Pickup Datetime',value="2015-01-27 13:08:24 UTC")
        pickup_latitude = st.number_input('Pickup Latitude',value=40.7638053894043,min_value=-90.0,max_value=90.0)
        pickup_longitude = st.number_input('Pickup Longitude',value=-73.973320007324219,min_value=-180.0,max_value=180.0)
        dropoff_latitude = st.number_input('Dropoff Latitude',value=40.74383544921875,min_value=-90.0,max_value=90.0)
        dropoff_longitude = st.number_input('Dropoff Longitude',value=-73.981430053710938,min_value=-180.0,max_value=180.0)
        passenger_count = st.number_input('Passenger Count',min_value=1,max_value=6)

        features = {
                "pickup_datetime": pickup_datetime,
                "pickup_latitude" : pickup_latitude,
                "pickup_longitude" : pickup_longitude,
                "dropoff_latitude" : dropoff_latitude,
                "dropoff_longitude" : dropoff_longitude,
                "passenger_count" : passenger_count
            }
            
        
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            data = requests.post(url=concat(request_url, "/predict"), json=features).json()
            if data:
                print(data)
                st.metric(label="Predicted Taxi Fare",value=round(data['Fare'],2))
            else:
                st.error("Error")


if __name__ == '__main__':
    main()