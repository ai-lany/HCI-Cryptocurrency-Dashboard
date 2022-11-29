from flask import Flask
import requests
import json
import streamlit as st
import pandas as pd
import numpy as np
import utils
import os

API_KEY = '5ae705c7-4dbf-4eba-ae61-183c137c4400'
COUNTRIES_URL = 'https://api.airvisual.com/v2/countries?key={}'.format(API_KEY)



@st.cache(allow_output_mutation=True)
def getCountries():
    response = requests.get(COUNTRIES_URL).json()
    print(response)
    return response

@st.cache(allow_output_mutation=True)
def getStates(country):
    print('getStates')
    STATES_URL = 'https://api.airvisual.com/v2/states?country={}&key={}'.format(country,API_KEY)
    response = requests.get(STATES_URL).json()
    print(response)
    return response

@st.cache(allow_output_mutation=True)
def getCities(country, state):
    print('getCities')
    CITY_URL = 'https://api.airvisual.com/v2/cities?state={}&country={}&key={}'.format(state,country,API_KEY)
    print(CITY_URL)
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


st.title('Air Quality')

COUNTRIES = getCountries()
DictList = list[dict[str,str]]
if COUNTRIES['status'] != 'success':
    COUNTRIES = getDataFromFile('countries.JSON')
COUNTRIES_LIST:DictList = COUNTRIES['data']  

country =  st.selectbox(
            'Country',
            [c['country'] for c in COUNTRIES_LIST],
            index=134
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
        airQuality = getAirQuality(country, state, city)
        print(airQuality)
        coordinates = airQuality['data']['location']['coordinates']
        utils.map_creator(coordinates[0],coordinates[1])
