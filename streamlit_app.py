import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import altair as alt
import sqlite3
import calendar
from ml_model import *
import streamlit.components.v1 as components

st.title("Let's analyze some Crime Data 📊.")


# chart = alt.Chart(df).mark_bar().encode(
#     x=alt.X("district:O", sort='y'),
#     y=alt.Y("count():Q"),
#     color='arrest',
#     tooltip='count()'
# ).interactive()




#########################
###  counts by month  ###
######################### 
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

# The basic line
line = alt.Chart(source).mark_line(interpolate='basis').encode(
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

###############################
###  district map & counts  ###
###############################

# @st.cache  # add caching so we load the data only once
def load_district_count():
    # url for district arrests
    # crime_url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json?$select=district,count(district),sum(case(arrest='1',1,true,0))&$group=district"
    crime_url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json?$select=year,district,count(district)&$group=year,district"
    df_district_count = pd.read_json(crime_url)
    df_district_count['district'] = df_district_count['district'].dropna().astype(int).astype(str)

    url_geojson = "https://data.cityofchicago.org/resource/24zt-jpfn.geojson"
    data_geojson_remote = alt.Data(url=url_geojson, format=alt.DataFormat(property='the_geom',type='json'))
    stations = pd.read_json("https://data.cityofchicago.org/resource/z8bn-74gv.json?$select=district,latitude,longitude")
    stations = stations[stations['district'] != 'Headquarters'] 

    st.write(type(stations['district']))
    st.write(type(df_district_count['district']))
    data = pd.merge(stations, df_district_count, on='district')

    return data

data = load_district_count()

url_geojson = "https://data.cityofchicago.org/resource/24zt-jpfn.geojson"
data_geojson_remote = alt.Data(url=url_geojson, format=alt.DataFormat(property='the_geom',type='json'))

# chart object
district_map = alt.Chart(data_geojson_remote).mark_geoshape(
    fill='lightgray',
    stroke='white'
)

# Points and text
hover = alt.selection(type='single', on='mouseover', nearest=True,
                      fields=['latitude', 'longitude', 'district'])
selector = selector = alt.selection_single(empty='all', fields=['district'])

base = alt.Chart(data).encode(
    longitude='longitude:Q',
    latitude='latitude:Q',
).properties(
    width=100
)

text = base.mark_text(dx=10, dy=-10, align='right').encode(
    alt.Text('district', type='nominal')
)

points = base.mark_point().encode(
    color=alt.condition(~selector, alt.value('gray'), alt.value('#F63366')),
    size=alt.condition(~hover, alt.value(30), alt.value(100)),
).add_selection(hover, selector)

### graph of counts by district over time
start_year, end_year = st.slider("Start Year", 2001, 2020, (2001, 2020))

chart = alt.Chart(data).mark_line().transform_filter(
    (start_year <= alt.datum['year']) & (end_year >= alt.datum['year'])
).encode(
    x='year:O',
    y='count_district',
    color=alt.condition(~selector, 'district:O', alt.value('#F63366'))
).add_selection(selector)

st.write(district_map + points + text | chart)
# # select district
# district_values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '14', '15', '16', '17', '18', '19', '20', '22', '24', '25']
# options = list(range(len(district_values)))
# select_district = st.selectbox("district", options, format_func=lambda x: district_values[x])

# st.write(district_values[select_district])


###############################
###        ML models        ###
###############################

st.sidebar.write(comp)

# select crime type
type_values = ['arson', 'assault', 'battery', 'burglary', 'concealed carry license violation', 'criminal damage', 'criminal sexual assault', 'criminal trespass', 'crim sexual assault', 'deceptive practice', 'domestic violence', 'gambling', 
'homicide', 'human trafficking', 'interference with public officer', 'intimidation', 'kidnapping', 'liquor law violation', 'motor vehicle theft', 'narcotics', 'non - criminal', 'non-criminal', 'non-criminal (subject specified)', 'obscenity', 'offense involving children', 'other narcotic violation', 'other offense', 'prostitution', 'public indecency', 'public peace violation', 'ritualism', 'robbery', 'sex offense', 'stalking', 'theft', 'weapons violation']
options = list(range(len(type_values)))
select_type = st.sidebar.selectbox("crime type", options, format_func=lambda x: type_values[x])

# st.write(type_values[select_type])

# select community area
beat_values = [111, 112, 113, 114, 121, 122, 123, 124, 131, 132, 133, 134, 211, 212, 213, 214, 215, 221, 222, 223, 224, 225, 231, 232, 233, 234, 235, 310, 311, 312, 313, 314, 321, 322, 323, 324, 331, 332, 333, 334, 411, 412, 413, 414, 421, 
422, 423, 424, 430, 431, 432, 433, 434, 511, 512, 513, 522, 523, 524, 531, 532, 533, 611, 612, 613, 614, 621, 622, 623, 624, 631, 632, 633, 634, 711, 712, 713, 714, 715, 722, 723, 724, 725, 726, 731, 732, 733, 734, 735, 811, 812, 813, 814, 815, 821, 822, 823, 824, 825, 831, 832, 833, 834, 835, 911, 912, 913, 914, 915, 921, 922, 923, 924, 925, 931, 932, 933, 934, 935, 1011, 1012, 1013, 1014, 1021, 1022, 1023, 1024, 1031, 1032, 1033, 1034, 1111, 1112, 1113, 1114, 1115, 1121, 1122, 1123, 1124, 1125, 1131, 1132, 1133, 1134, 1135, 1211, 1212, 1213, 1214, 1215, 1221, 1222, 1223, 1224, 1225, 1231, 1232, 1233, 1234, 1235, 1311, 1312, 1313, 1322, 1323, 1324, 1331, 1332, 1333, 1411, 1412, 1413, 1414, 1421, 1422, 1423, 1424, 1431, 1432, 1433, 1434, 1511, 1512, 1513, 1522, 1523, 1524, 1531, 1532, 1533, 1611, 1612, 1613, 1614, 1621, 1622, 1623, 1624, 1631, 1632, 1633, 1634, 1651, 1652, 1653, 1654, 1655, 
1711, 1712, 1713, 1722, 1723, 1724, 1731, 1732, 1733, 1811, 1812, 1813, 1814, 1821, 1822, 1823, 1824, 1831, 1832, 1833, 1834, 1911, 1912, 1913, 1914, 1915, 1921, 1922, 1923, 1924, 1925, 1931, 1932, 1933, 1934, 1935, 2011, 2012, 2013, 2022, 2023, 2024, 2031, 2032, 2033, 2111, 2112, 2113, 2122, 2123, 2124, 2131, 2132, 2133, 2211, 2212, 2213, 2221, 2222, 2223, 2232, 2233, 2234, 2311, 2312, 2313, 2322, 2323, 2324, 2331, 2332, 2333, 2411, 2412, 2413, 2422, 2423, 2424, 2431, 2432, 2433, 2511, 2512, 2513, 2514, 2515, 2521, 2522, 2523, 2524, 2525, 2531, 2532, 2533, 2534, 2535]
options = list(range(len(beat_values)))
select_beat = st.sidebar.selectbox("beat", options, format_func=lambda x: beat_values[x])

domestic = st.sidebar.checkbox("Domestic")

crime_input = pd.DataFrame(columns = cols)
crime_input.loc[0, 'primary_type'] = type_values[select_type]
crime_input.loc[0, 'domestic'] = domestic
crime_input.loc[0, 'beat'] = beat_values[select_beat]
crime_input.loc[0, 'year'] = 2020
st.sidebar.write(crime_input)


st.sidebar.text("")
st.sidebar.text("")
predicted = clf.fit(X_train, y_train).predict(crime_input.loc[[0]])
if predicted:
    st.sidebar.text("prediction: Arrested!")
else:
    st.sidebar.text("prediction: Not Arrested!")

