from operator import concat
import streamlit as st
import requests
import os


def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}


def main():
    request_url = "https://fastapi-taxi-fare-vishank-betatest-ws.tfy-ctl-euwe1-develop.develop.truefoundry.tech"
    st.set_page_config(page_title="Taxi Fare", page_icon="🚕")
    st.title("Taxi Fare Prediction")
    session = requests.Session()
    with st.form("my_form"):
        
        pickup_datetime = st.text_input('Pickup Datetime')
        pickup_latitude = st.number_input('Pickup Latitude')
        pickup_longitude = st.number_input('Pickup Longitude')
        dropoff_latitude = st.number_input('Dropoff Latitude')
        dropoff_longitude = st.number_input('Dropoff Longitude')
        passenger_count = st.number_input('Passenger Count')

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
            data = requests.post(url=concat(request_url, "/infer"), json=features).json()
            if data:
                print(data)
                st.metric(label="Predicted Taxi Fare",value=round(data['Fare'],2))
            else:
                st.error("Error")


if __name__ == '__main__':
    main()