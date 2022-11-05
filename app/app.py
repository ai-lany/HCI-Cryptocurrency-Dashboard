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


with open('./data/coins.json') as fp:
    coins = json.load(fp)
with open('./data/ATMs.json') as fp:
    atm_locations = json.load(fp)


COINTODATA = {
    "Bitcoin":coins["Bitcoin"],
    "Ethereum":coins["Ethereum"],
    "Solana":coins["Solana"]
}

fake = Faker()

def get_chart(data):
    hover = alt.selection_single(
        fields=["time"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data).mark_line(color=color,).encode( 
            alt.Y('Price',scale=alt.Scale(zero=False) ), 
            x='Time',
        )
    )
    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65,color=color)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="Time",
            y="Price",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Time", title="Date"),
                alt.Tooltip("Price", title="Price (USD)"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()


# Using "with" notation
with st.sidebar:

    #Buy/sell widget
    st.title('Trade Bitcoin')
    number = st.number_input("Bitcoin Amount", min_value=0.0, step=0.1)
    st.text(str(round(COINTODATA["Bitcoin"]["prices"][0][1]*number,2)) + " USD")
    st.caption("Minimum of $3.00 USD required.")


    
    col1, col2 = st.columns([1, 1])
    if st.button("Buy BTC", key="Buy", type="primary"):
        st.session_state.number = number
        if number > 3/COINTODATA["Bitcoin"]["prices"][0][1]*number:

            st.write(round(number, 4) ,'BTC has been purchased and will appear in your account shortly.')
            st.success('Thank you!', icon="✅")
        
        elif number != 0.0:
            st.error('Unable to process: Amount is below $3.00 USD', icon="🚨")   
        else:
            st.error('Unable to process: Zero amount', icon="🚨")  

    if st.button("Sell BTC", key="Sell", type="secondary"):
        if number > 0:

            st.write(round(number,4),' BTC has been sold and will be sent to your bank account in 3-5 business days.')
            st.success('Thank you!', icon="✅")
        else:
            st.error('Unable to process: Zero amount', icon="🚨")  

    #Map of Bitcoin ATM's
    st.write("")
    st.title("Bitcoin ATM's")
    container = st.container()
    map_df = pd.DataFrame(
        atm_locations["bitcoin"],
        columns=['lat', 'lon'])
    container.map(map_df,12)



st.header("CoinWatch")
st.caption("Get information about your favorite cryptocurrencies!")
#Dropdown menu for different coins
option = st.selectbox(
    'Token',
    ('Bitcoin', 'Ethereum', 'Solana')
)
st.caption("Select a coin to get started.")
st.write("")

if(COINTODATA[option] is not None):

    #Header 
    col1, col2,col3 = st.columns([1, 7,1])

    with col1:
        st.image(COINTODATA[option]["image"], caption=None, width=64)

    with col2:
        st.title(option)

    with col3:
        #Color picker for graph line color
        color = st.color_picker('Pick A Color', '#FF65A8')
        st.session_state.color=color


    prices = [round(i[1],2) for i in COINTODATA[option]["prices"]]
    btc_times = [i[0] for i in COINTODATA[option]["prices"]]

    index=pd.date_range("2022-11-02", periods=len(prices), freq="H")
    prices_df = pd.DataFrame({ 
        "Time":index,
        "Price":prices,
    })

    btc_mCap = [round(i[1]/20000000,2) for i in COINTODATA[option]["market_caps"]]
    total_volumes = [round(i[1]/20000000,2) for i in COINTODATA[option]["total_volumes"]]
    btc_times = [i[0] for i in COINTODATA[option]["market_caps"]]


    st.altair_chart(get_chart(prices_df),use_container_width=True)

    mCap_df = pd.DataFrame({ 
        "Time":index,
        "Market Cap":btc_mCap,
    })
    vol_df = pd.DataFrame({ 
        "Time":index,
        "Total Volume":total_volumes,
    })
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Market Cap")
        x = alt.Chart(mCap_df).mark_line(color=color,).encode( alt.Y('Market Cap',scale=alt.Scale(zero=False) ), x='Time')
        st.altair_chart(x, use_container_width=True)
    with col2:
        st.subheader("Market Cap")
        y = alt.Chart(vol_df).mark_line(color=color,).encode( alt.Y('Total Volume',scale=alt.Scale(zero=False) ), x='Time')
        st.altair_chart(y, use_container_width=True)

    st.write("")
    st.header("Coins")
    df = pd.DataFrame(
    [
        ["Bitcoin", COINTODATA["Bitcoin"]["prices"][0][1],COINTODATA["Bitcoin"]["market_caps"][0][1],COINTODATA["Bitcoin"]["total_volumes"][0][1]],
        ["Ethereum", COINTODATA["Ethereum"]["prices"][0][1],COINTODATA["Ethereum"]["market_caps"][0][1],COINTODATA["Ethereum"]["total_volumes"][0][1]],
        ["Solana", COINTODATA["Solana"]["prices"][0][1],COINTODATA["Solana"]["market_caps"][0][1],COINTODATA["Solana"]["total_volumes"][0][1]]
        ],
    columns=(["Coin", "Price", "Market Cap", "Total Volume"])
    )

    st.dataframe(df, use_container_width=True)  # Same as st.write(df)




review = st.select_slider(
    '⭐ Please rate your experience ⭐',
    options=[' ', '⭐', '⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'])

st.caption('(Optional)')
revTxt = st.text_area('Is there anything we need to improve on?', '')



if st.button("Submit", key="SubmitReview", type="secondary"):

    if review != ' ':
        st.success('Thank you!', icon="✅")
        st.balloons()

