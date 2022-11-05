from flask import Flask
import requests
import json
import streamlit as st
import pandas as pd
import numpy as np
import rich
import altair as alt
from bokeh.plotting import figure
from faker import Faker



APIURL = "https://api.coingecko.com/api/v3"
COINTOURL = {
    "Bitcoin":"/coins/bitcoin/",
}
with open('./data/bitcoin.json') as fp:
    btc_chart = json.load(fp)
with open('./data/ATMs.json') as fp:
    atm_locations = json.load(fp)



fake = Faker()
# def getChartData(coin, numDays):
#     response = requests.get(APIURL+COINTOURL.get(coin)+ "/market_chart?vs_currency=usd&days=" + numDays)
#     if(response.status_code != 200):
#         return
#     data = response.text
#     return json.loads(data)



# Using "with" notation
with st.sidebar:
    #Map of Bitcoin ATM's
    st.header("Bitcoin ATM's")
    container = st.container()
    map_df = pd.DataFrame(
        atm_locations["bitcoin"],
        columns=['lat', 'lon'])
    container.map(map_df,12)


if(btc_chart is not None):
    btc_prices = [round(i[1],2) for i in btc_chart["prices"]]
    btc_times = [i[0] for i in btc_chart["prices"]]

    index=pd.date_range("2022-11-02", periods=len(btc_prices), freq="H")
    prices_df = pd.DataFrame({ 
        "time":index,
        "price":btc_prices,
    })

    btc_mCap = [round(i[1],2) for i in btc_chart["market_caps"]]
    btc_times = [i[0] for i in btc_chart["market_caps"]]

    mCap_df = pd.DataFrame({ 
        "time":index,
        "market_caps":btc_mCap,
    })
    
    #Header 
    col1, col2 = st.columns([1, 7])

    with col1:
        st.image(btc_chart["image"], caption=None, width=64)

    with col2:
        st.title("Bitcoin")



    
    #Selectors
    col1, col2 = st.columns([7, 1])

    with col1:
        #Dropdown menu for different coins
        option = st.selectbox(
            'Token',
            ('Bitcoin', 'Ethereum', 'XRP'))

    with col2:
        #Color picker for graph line color
        color = st.color_picker('Pick A Color', '#F3585A')



    a = alt.Chart(prices_df).mark_line(color=color,).encode( alt.Y('price',scale=alt.Scale(zero=False) ), x='time')
    st.altair_chart(a, use_container_width=True)


    x = alt.Chart(mCap_df).mark_line(color=color,).encode( alt.Y('market_caps',scale=alt.Scale(zero=False) ), x='time')

    #Market Cap Checkbox
    mCapBTC = st.checkbox('Show Market Cap', key="MC")

    if mCapBTC:
        st.altair_chart(x, use_container_width=True)


#Selectors
col1, col2 = st.columns([5, 5])

with col1:
    st.header("Coins")
    df = pd.DataFrame(
    [
        ["Bitcoin", btc_chart["prices"][0][1],btc_chart["market_caps"][0][1]],
        ["Ethereum", btc_chart["prices"][0][1],btc_chart["market_caps"][0][1]],
        ["XRP", btc_chart["prices"][0][1],btc_chart["market_caps"][0][1]]
        ],
    columns=(["Coin", "Price", "Market Cap"])
    )

    st.dataframe(df)  # Same as st.write(df)
with col2:
    st.write("Placeholder")


