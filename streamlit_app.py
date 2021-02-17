import streamlit as st
import pandas as pd
import altair as alt
from ml_model import *

#### Title ####

st.title("How To Get Away With Murder: Data Edition")
st.write("If Batman were to study data visualization, it might look something like this.")
st.markdown("<p>Data taken from the <a href='https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present-Dashboard/5cd6-ry5g'>Chicago Crimes Dataset.</a></p>", unsafe_allow_html = True)

@st.cache  # add caching so we load the data only once
def load_data(url):
    # Load the crime data from https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present-Dashboard/5cd6-ry5g
    df = pd.read_json(url)
    df.columns = ['year', 'primary_type', 'num_crimes', 'num_arrests']
    df['arrest_rate'] = df['num_arrests']/df['num_crimes']
    df['crime_rate'] = df['num_crimes']
    return df
crime_url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json?$select=year,primary_type,count(primary_type),sum(case(arrest='1',1,true,0))&$group=primary_type,year"
df = load_data(crime_url)

#### Analysis Intro ####
st.markdown("<h2>Overall Crime Frequencies</h2>", unsafe_allow_html=True)
st.write("What is the current trend with the number of crimes in Chicago? Is this trend similarly reflected within each type of crime as well?")
st.write("Click on multiple types of crimes to see the changes in frequency over time for each type.")



selection = alt.selection_multi(fields=['primary_type'])

chart3 = alt.Chart(df).mark_area().encode(
    alt.X("year:O"),
    alt.Y("num_crimes:Q", stack='center', axis=None),
    alt.Color("primary_type:N", scale=alt.Scale(scheme='category20b'), legend=None),
    opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
    tooltip='primary_type'
).add_selection(
    selection
)

background = alt.Chart(df).mark_bar().encode(
    alt.X('year:O'),
    alt.Y('sum(num_crimes):Q'),
    color=alt.value('#ddd')
)

hists = chart3.mark_bar(opacity=0.5, thickness=100).encode(
    alt.X('year:O'),
    alt.Y('num_crimes:Q'),
    color=alt.Color('primary_type:N', scale=alt.Scale(scheme='category20b'), legend=None)
).transform_filter(
    selection
)


#highlight = hist_base.transform_filter(selection)


st.write(chart3 | background + hists)


# chart = alt.Chart(df).mark_area().encode(
#     alt.X("Year:T", axis=alt.Axis(domain=False, format='%Y', tickSize=0)),
#     alt.Y("count(Year):Q"),
#     alt.Color("Primary Type:N", scale=alt.Scale(scheme='category20b')),
#     opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
# ).add_selection(
#     selection
# )

#### Number of Crimes vs. Arrest Rates ####
st.markdown("<h2>Arrest Rates Over Time</h2>", unsafe_allow_html=True)
st.write("Now that we've explored changes in types of crime over time, what is the trend for frequency of crimes and arrest rates?")
st.write("Hover over each line to see change in frequency and arrest rate for that particular type of crime.")

#crime_url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json?$select=district,count(district),sum(case(arrest='1',1,true,0))&$group=district"
#return pd.read_json(crime_url)

highlight = alt.selection(type='single', on='mouseover', fields=['primary_type'], nearest=True)

crimes_base = alt.Chart(df).encode(
    alt.X('year:O'),
    alt.Y('num_crimes:Q'),
    alt.Color('primary_type:N',legend=None),
    tooltip='primary_type:N'
)

crimes_points = crimes_base.mark_circle().encode(
    opacity=alt.value(0)
).add_selection(
    highlight
)

crimes_lines = crimes_base.mark_line(interpolate='basis').encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(3)),
    opacity=alt.condition(highlight, alt.value(1), alt.value(0.3))
)

arrests_base = alt.Chart(df).encode(
    alt.X('year:O'),
    alt.Y('arrest_rate:Q'),
    alt.Color('primary_type:N', legend=None),
    tooltip='primary_type:N'
)

arrests_points = arrests_base.mark_circle().encode(
    opacity=alt.value(0)
).add_selection(
    highlight
)

arrests_lines = arrests_base.mark_line(interpolate='basis').encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(3)),
    opacity=alt.condition(highlight, alt.value(1), alt.value(0.3))
)

st.write(crimes_points+crimes_lines | arrests_points+arrests_lines)

#### Mapping Crimes ####
st.markdown("<h2>Location of Arrests</h2>", unsafe_allow_html=True)
st.write("What is the distribution of crimes over the city?")
st.write("Pan over the map to select an area to view and adjust the range of year.")

#chart.encode(y='num_crimes:Q') | chart.encode(y="arrest_rate:Q")
#st.write(chart)

#categorical_arrests = load_data('https://data.cityofchicago.org/resource/ijzp-q8t2.json?$select=year,primary_type,sum(case(arrest=%271%27,1,true,0)),count(arrest)&$group=year,primary_type')
#categorical_arrests.columns = ['year', 'primary_type', 'arrests', 'number of crimes']
#st.write(categorical_arrests)

nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['year'], empty='none')

line = alt.Chart(df, height=600, width=800).mark_line(interpolate='basis').encode(
    alt.X("year:O"),
    alt.Y('arrest_rate:Q'),
    alt.Color("primary_type:N", scale=alt.Scale(scheme='category20b'))
)

selectors = alt.Chart(df).mark_point().encode(
    x='year:O',
    opacity=alt.value(0),
).add_selection(
    nearest
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# Draw text labels near the points, and highlight based on selection
text = line.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'arrest_rate:Q', alt.value(' '))
)

# Draw a rule at the location of the selection
rules = alt.Chart(df).mark_rule(color='gray').encode(
    x='year:O',
).transform_filter(
    nearest
)

chart2 = alt.layer(
    line, selectors, points, rules, text
).properties(
    width=600, height=300
)

#st.write(chart2)




@st.cache
def load_coordinate_data(url):
    df = pd.read_json(url)
    df.columns = ['year', 'x_coordinate','freq', 'y_coordinate', 'y_freq']
    df = df.drop(columns=['y_freq'])
    df = df.dropna(axis=0)
    df = df[df['x_coordinate'] > 0]
    return df

location_url = 'https://data.cityofchicago.org/resource/ijzp-q8t2.json?$select=year,x_coordinate,count(x_coordinate),y_coordinate,count(y_coordinate)&$group=year,x_coordinate,y_coordinate'
coordinate_df = load_coordinate_data(location_url)

#st.write(coordinate_df)

brush = alt.selection(type='interval')
start_year, end_year = st.slider("Years", 2001, 2020, (2001, 2020))


location_chart = alt.Chart(coordinate_df).mark_point().transform_filter(
    (start_year <= alt.datum['year']) & (end_year >= alt.datum['year'])).encode(
    alt.X('x_coordinate:Q', scale=alt.Scale(domain=(1100000,1205000))),
    alt.Y('y_coordinate:Q', scale=alt.Scale(domain=(1810000,1960000)))
).add_selection(brush)




count_chart = alt.Chart(coordinate_df).mark_point().transform_filter(
    (start_year <= alt.datum['year']) & (end_year >= alt.datum['year'])).encode(
    alt.X('x_coordinate:Q', scale=alt.Scale(domain=(1100000,1205000))),
    alt.Y('y_coordinate:Q', scale=alt.Scale(domain=(1810000,1960000))),
    size='sum(freq):Q'
).transform_filter(brush)

st.write(location_chart | count_chart)

@st.cache
def load_district_data(url):
    df = pd.read_json(url)
    df.columns = ['year','district','freq','arrests']
    df['arrest_rate'] = df['arrests']/df['freq']
    return df

#district_data = load_district_data("https://data.cityofchicago.org/resource/ijzp-q8t2.json?$select=year,district,count(year),sum(case(arrest='1',1,true,0))&$group=year,district")

#st.write(district_data)

#### District Breakdown ####
st.markdown("<h2>Frequency of Crime and Arrest Rate per District</h2>", unsafe_allow_html=True)
st.write("How do districts differ in terms of frequency of crime? Do all districts have similar arrest rates?")
st.write("Click on a district or a line representing a district to highlight it. The average across all districts is marked in red.")

@st.cache  # add caching so we load the data only once
def load_district_arrests():
    # url for district arrests
    crime_url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json?$select=year,district,count(district),sum(case(arrest='1',1,true,0))&$group=year,district"
    #crime_url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json?$select=year,district,count(district)&$group=year,district"
    df_district_count = pd.read_json(crime_url)
    df_district_count['district'] = df_district_count['district'].dropna().astype(int).astype(str)

    url_geojson = "https://data.cityofchicago.org/resource/24zt-jpfn.geojson"
    data_geojson_remote = alt.Data(url=url_geojson, format=alt.DataFormat(property='the_geom',type='json'))
    stations = pd.read_json("https://data.cityofchicago.org/resource/z8bn-74gv.json?$select=district,latitude,longitude")
    stations = stations[stations['district'] != 'Headquarters'] 

    #st.write(type(stations['district']))
    #st.write(type(df_district_count['district']))
    data = pd.merge(stations, df_district_count, on='district')
    data.columns = ['district','latitude','longitude','year','count_district','arrests']
    data['arrest_rate'] = data['arrests']/data['count_district']

    return data

data = load_district_arrests()
#st.write(data)

#### new stuff from vivian ####

url_geojson = "https://data.cityofchicago.org/resource/24zt-jpfn.geojson"
data_geojson_remote = alt.Data(url=url_geojson, format=alt.DataFormat(property='the_geom',type='json'))
stations = pd.read_json("https://data.cityofchicago.org/resource/z8bn-74gv.json")
stations = stations[stations['district'] != 'Headquarters'] 
# print(stations)

#st.write(stations)



#url_geojson = "https://data.cityofchicago.org/resource/24zt-jpfn.geojson"
data_geojson_remote = alt.Data(url=url_geojson, format=alt.DataFormat(property='the_geom',type='json'))

# chart object
district_map = alt.Chart(data_geojson_remote).mark_geoshape(
    fill='lightgray',
    stroke='white'
)

# Points and text
hover = alt.selection(type='single', on='mouseover', nearest=True,
                      fields=['latitude', 'longitude','district'])
selector = alt.selection_single(empty='all', fields=['district'])

base = alt.Chart(data).encode(
    longitude='longitude:Q',
    latitude='latitude:Q',
)

text = base.mark_text(dx=10, dy=-10, align='right').encode(
    alt.Text('district', type='nominal')
)

points = base.mark_point().encode(
    color=alt.condition(~selector, alt.value('gray'), alt.value('red')),
    size=alt.condition(~hover, alt.value(30), alt.value(100)),
).add_selection(hover, selector)

### graph of counts by district over time
start_year, end_year = st.slider("Start Year", 2001, 2020, (2001, 2020))

base = alt.Chart(data).mark_line(interpolate='basis').transform_filter(
    (start_year <= alt.datum['year']) & (end_year >= alt.datum['year'])
)

new_points = alt.Chart(data).mark_circle().encode(
    opacity=alt.value(0)
).add_selection(
    hover
)

new_lines = alt.Chart(data).mark_line(interpolate='basis').encode(
    size=alt.condition(~hover, alt.value(1), alt.value(3)),
    opacity=alt.condition(hover, alt.value(1), alt.value(0.3))
)

avg_count = base.encode(
    x='year:O',
    y='mean(count_district)',
    color=alt.value('#F63366')
)

new_chart = base.encode(
    x='year:O',
    y='count_district',
    color='district',
    opacity=alt.condition(selector,alt.value(1),alt.value(0.2)),
    tooltip='district'
).add_selection(selector)



avg_arrests = base.encode(
    x='year:O',
    y='mean(arrest_rate)',
    color=alt.value('#F63366')
)

new_arrests = base.encode(
    x='year:O',
    y='arrest_rate:Q',
    color='district',
    opacity=alt.condition(selector,alt.value(1),alt.value(0.2)),
    tooltip='district'
).add_selection(selector)

arrests = alt.Chart(data).mark_line(interpolate='basis').transform_filter(
    (start_year <= alt.datum['year']) & (end_year >= alt.datum['year'])
).encode(
    x='year:O',
    y='arrest_rate:Q',
    color=alt.condition(~selector, 'district:O', alt.value('red')),
    opacity=alt.condition(selector,alt.value(1),alt.value(0.3))
)

st.write(district_map + points + text | new_chart + avg_count | new_arrests + avg_arrests)


###############################
###        ML models        ###
###############################

#st.sidebar.write(comp)

st.sidebar.title("Would you be arrested?")
st.sidebar.write("Enter your own data here and see.")

# select crime type
type_values = ['ARSON', 'ASSAULT', 'BATTERY', 'BURGLARY', 'CONCEALED CARRY LICENSE VIOLATION', 'CRIM SEXUAL ASSAULT', 'CRIMINAL DAMAGE', 'CRIMINAL SEXUAL ASSAULT', 'CRIMINAL TRESPASS', 'DECEPTIVE PRACTICE', 'GAMBLING', 'HOMICIDE', 'HUMAN TRAFFICKING', 'INTERFERENCE WITH PUBLIC OFFICER', 
'INTIMIDATION', 'KIDNAPPING', 'LIQUOR LAW VIOLATION', 'MOTOR VEHICLE THEFT', 'NARCOTICS', 'NON-CRIMINAL', 'OBSCENITY', 'OFFENSE INVOLVING CHILDREN', 'OTHER NARCOTIC VIOLATION', 'OTHER OFFENSE', 'PROSTITUTION', 'PUBLIC INDECENCY', 'PUBLIC PEACE VIOLATION', 'ROBBERY', 'SEX OFFENSE', 'STALKING', 'THEFT', 'WEAPONS VIOLATION']
options = list(range(len(type_values)))
select_type = st.sidebar.selectbox("crime type", options, format_func=lambda x: type_values[x])

district_values = [1,2,3,4,5,6,7,8,9,10,11,12,14,15,16,17,18,19,20,21,22,24,25]
district_options = list(range(len(district_values)))
select_district = st.sidebar.selectbox("district", district_options, format_func=lambda x: district_values[x])

domestic = st.sidebar.checkbox("Domestic")

crime_input = pd.DataFrame()
crime_input.loc[0, 'Primary Type'] = type_values[select_type]
crime_input.loc[0, 'Domestic'] = domestic
crime_input.loc[0, 'District'] = district_values[select_district]
crime_input.loc[0, 'Year'] = 2020
print('new')

# crime_input.loc[0, 'year'] = 2020
st.sidebar.write(crime_input.loc[[0]])


st.sidebar.text("")
st.sidebar.text("")

predicted = model.predict(crime_input.loc[[0]])
if predicted:
    st.sidebar.markdown("<h4>Prediction: Arrested</h4>", unsafe_allow_html=True)
else:
    st.sidebar.markdown("<h4>Prediction: Not Arrested</h4>", unsafe_allow_html=True)