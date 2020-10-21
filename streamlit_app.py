import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import altair as alt
import sqlite3
import calendar

st.title("Let's analyze some Crime Data 📊.")

@st.cache  # add caching so we load the data only once
def load_data():
    # url for district arrests
    # crime_url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json?$select=district,count(district),sum(case(arrest='1',1,true,0))&$group=district"
    crime_url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json?$select=year,count(year)&$group=year"
    return pd.read_json(crime_url)

@st.cache
def load_map():
    return alt.InlineData(values="https://data.cityofchicago.org/resource/24zt-jpfn.json", format=alt.DataFormat(property='the_geom',type='json'))
    return alt.Data(url="https://data.cityofchicago.org/resource/24zt-jpfn.json$select=district,count(district),sum(arrest)&$group=district", format=alt.DataFormat(property='the_geom',type='json'))


df = load_data()
# df["arrest_ratio"] = df["district"] + df["ward"]

st.write("Let's look at raw data in the Pandas Data Frame.")

st.write(df)

# st.write(gdf)

# choro = alt.Chart(gdf).mark_geoshape(
#     stroke='black'
# ).properties( 
#     width=650,
#     height=800
# )
# st.write(choro)

# chart = alt.Chart(df).mark_bar().encode(
#     x=alt.X("district:O", sort='y'),
#     y=alt.Y("count():Q"),
#     color='arrest',
#     tooltip='count()'
# ).interactive()




#####################
###    CHART 2    ###
#####################
@st.cache  # add caching so we load the data only once
def load_data2():
    # url for district arrests
    # crime_url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json?$select=district,count(district),sum(case(arrest='1',1,true,0))&$group=district"
    crime_url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json?$select=min(year),min(date_extract_m(date)),date_trunc_ym(date),count(date_trunc_ym(date))&$group=date_trunc_ym(date)&$order=date_trunc_ym(date)"
    df = pd.read_json(crime_url)
    df = df.rename(columns={'min_date_extract_m_date': 'month', 'date_trunc_ym_date': 'year_month', 'count_date_trunc_ym_date': 'count', 'min_year': 'year'})
    df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])
    return df

source = load_data2()
st.write(source)

# Create a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['year_month'], empty='none')

start_year, end_year = st.slider("Start Year", 2001, 2020, (2001, 2020))

# The basic line
line = alt.Chart(source).mark_line(interpolate='basis').transform_filter(
    (start_year <= alt.datum['year']) & (end_year >= alt.datum['year'])
).encode(
    x='year_month:T',
    y='count:Q',
).properties(
    width=600, height=300
)

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = alt.Chart(source).mark_point().encode(
    x='year_month:T',
    opacity=alt.value(0),
).add_selection(
    nearest
).properties(
    width=600, height=300
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
).properties(
    width=600, height=300
)

# Draw text labels near the points, and highlight based on selection
month_text = line.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'month:O', alt.value(' '))
).properties(
    width=600, height=300
)
count_text = line.mark_text(align='left', dx=5, dy=5).encode(
    text=alt.condition(nearest, 'count:Q', alt.value(' '))
).transform_calculate(label='"count: " + datum.y').properties(
    width=600, height=300
)


# Draw a rule at the location of the selection
rules = alt.Chart(source).mark_rule(color='gray').encode(
    x='year_month:T',
).transform_filter(
    nearest
).properties(
    width=600, height=300
)

# Put the five layers into a chart and bind the data
chart2 = alt.layer(
    line, selectors, points, rules, count_text, month_text
).properties(
    width=600, height=300
)
st.write(chart2)

chart = alt.Chart(df).mark_line().transform_filter(
    (start_year <= alt.datum['year']) & (end_year >= alt.datum['year'])
).encode(
    x='year:O',
    y='count_year'
).properties( 
    width=650,
    height=400
)

st.write(chart)

url_geojson = "https://data.cityofchicago.org/resource/24zt-jpfn.geojson"
data_geojson_remote = alt.Data(url=url_geojson, format=alt.DataFormat(property='the_geom',type='json'))

# chart object
district_map = alt.Chart(data_geojson_remote).mark_geoshape(
).encode(
    color="DIST_NUM:O"
)
st.write(data_geojson_remote)
st.write(district_map)