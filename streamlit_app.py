import streamlit as st
import pandas as pd
import altair as alt

st.title("Let's analyze some Crime Data 📊.")

@st.cache  # add caching so we load the data only once
def load_data():
    # Load the crime data from https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present-Dashboard/5cd6-ry5g
    crime_url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json"
    return pd.read_csv(crime_url)

df = load_data()

st.write("Let's look at raw data in the Pandas Data Frame.")

st.write(df)

st.write("Hmm 🤔, is there some correlation between body mass and flipper length? Let's make a scatterplot with [Altair](https://altair-viz.github.io/) to find.")

chart = alt.Chart(df).mark_point().encode(
    x=alt.X("body_mass_g", scale=alt.Scale(zero=False)),
    y=alt.Y("flipper_length_mm", scale=alt.Scale(zero=False)),
    color=alt.Y("species")
).properties(
    width=600, height=400
).interactive()

st.write(chart)
