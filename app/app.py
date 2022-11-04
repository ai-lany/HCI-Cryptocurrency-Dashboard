from flask import Flask
import requests
import json
import streamlit as st
import pandas as pd
import numpy as np
import rich
import altair as alt
from bokeh.plotting import figure



APIURL = "https://api.coingecko.com/api/v3"
COINTOURL = {
    "Bitcoin":"/coins/bitcoin/",
}

# def getChartData(coin, numDays):
#     response = requests.get(APIURL+COINTOURL.get(coin)+ "/market_chart?vs_currency=usd&days=" + numDays)
#     if(response.status_code != 200):
#         return
#     data = response.text
#     return json.loads(data)



with open('bitcoin.json') as fp:
    btc_chart = json.load(fp)

if(btc_chart is not None):
    btc_prices = [round(i[1],2) for i in btc_chart["prices"]]
    btc_times = [i[0] for i in btc_chart["prices"]]
    index=pd.date_range("2022-11-02", periods=len(btc_prices), freq="H")
    df = pd.DataFrame(
       { "time":index,
        "price":btc_prices,
        
        }
    )
    
    st.header("Bitcoin")
    color = st.color_picker('Pick A Color', '#00f900')

    a = alt.Chart(df).mark_line(color=color,).encode( alt.Y('price',scale=alt.Scale(zero=False) ), x='time')
    st.altair_chart(a, use_container_width=True)
   




map_df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

#st.map(df)
option = st.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone'))

st.write('You selected:', option)


