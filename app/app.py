import requests
import json
import streamlit as st
import utils

API_KEY = '5ae705c7-4dbf-4eba-ae61-183c137c4400'
COUNTRIES_URL = 'https://api.airvisual.com/v2/countries?key={}'.format(API_KEY)
MIN_LAT = -90
MAX_LAT = 90
MIN_LONG = -180
MAX_LONG = 180


@st.cache(allow_output_mutation=True)
def getCountries():
    response = requests.get(COUNTRIES_URL).json()
    return response

@st.cache(allow_output_mutation=True)
def getStates(country):
    STATES_URL = 'https://api.airvisual.com/v2/states?country={}&key={}'.format(country,API_KEY)
    response = requests.get(STATES_URL).json()
    return response

@st.cache(allow_output_mutation=True)
def getCities(country, state):
    CITY_URL = 'https://api.airvisual.com/v2/cities?state={}&country={}&key={}'.format(state,country,API_KEY)
    response = requests.get(CITY_URL).json()
    return response

@st.cache(allow_output_mutation=True)
def getAirQuality(country, state, city):
    AIRQUALITY_URL = 'https://api.airvisual.com/v2/city?city={}&state={}&country={}&key={}'.format(city, state, country, API_KEY)
    response = requests.get(AIRQUALITY_URL).json()
    return response


def getDataFromFile(fileName):
    f = open(fileName)
    return json.load(f)

def celciusToFar(temp):
    return (temp * 9/5) + 32

st.title('Air Quality')

# Using "with" notation
with st.sidebar:

    latitude = st.number_input('Latitude')
    longitude = st.number_input('Longitude')
    if st.button('Get Air Quality', type="primary"):
        if latitude >= MIN_LAT and latitude <= MAX_LAT:
            if longitude >= MIN_LONG and longitude<= MAX_LONG:
                utils.map_creator(latitude,longitude)
            else:
                st.error('Longitude must be between -180 and 180.', icon="🚨")
        else:
            st.error('Latitude must be between -90 and 90.', icon="🚨")
    if st.button('Get Air Quality Near Me', type="secondary"):
        airQuality = getAirQuality('USA', 'Florida', 'Miami')
        coordinates = airQuality['data']['location']['coordinates']
        utils.map_creator(coordinates[0],coordinates[1])

        temperature = str(celciusToFar(airQuality['data']['current']['weather']['tp']))

        dateStr = "Today is "+ airQuality['data']['current']['pollution']['ts']

        airQualityStr = "The air quality index is: " +str(airQuality['data']['current']['pollution']['aqius']) 
        temperatureStr = "The temperature is: " + temperature
        humidityStr = "The humidity is: " + str(airQuality['data']['current']['weather']['hu'])
        
        st.caption(dateStr)
        st.info(airQualityStr, icon="ℹ️")
        st.info(temperatureStr, icon="ℹ️")
        st.info(humidityStr, icon="ℹ️")



COUNTRIES = getCountries()
DictList = list[dict[str,str]]
if COUNTRIES['status'] != 'success':
    COUNTRIES = getDataFromFile('countries.JSON')
COUNTRIES_LIST:DictList = COUNTRIES['data']  

country =  st.selectbox(
            'Country',
            [c['country'] for c in COUNTRIES_LIST],
            index=133
        )

st.write(country)
STATES = getStates(country)
STATES_LIST:DictList = STATES['data']  
if STATES['status'] == 'success':
    state =  st.selectbox(
                'State',
                [s['state'] for s in STATES_LIST]
            )
    st.write(state)
    
    CITIES = getCities(country, state)
    CITIES_LIST:DictList = CITIES['data']
    if CITIES['status'] == 'success':
        city = st.selectbox(
                'City',
                [c['city'] for c in CITIES_LIST]
            )
        airQualityData = getAirQuality(country, state, city)
        coordinates = airQualityData['data']['location']['coordinates']
        utils.map_creator(coordinates[0],coordinates[1])

        temperature = str(celciusToFar(airQualityData['data']['current']['weather']['tp']))

        dateStr = "Today is "+ airQualityData['data']['current']['pollution']['ts']

        airQualityStr = "The air quality index is: " +str(airQualityData['data']['current']['pollution']['aqius']) 
        temperatureStr = "The temperature is: " + temperature
        humidityStr = "The humidity is: " + str(airQualityData['data']['current']['weather']['hu'])
        
        st.caption(dateStr)
        st.info(airQualityStr, icon="ℹ️")
        st.info(temperatureStr, icon="ℹ️")
        st.info(humidityStr, icon="ℹ️")


