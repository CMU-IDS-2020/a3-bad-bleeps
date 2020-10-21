import streamlit as st
import pandas as pd
import altair as alt

st.title("Let's analyze some Crime Data 📊.")

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



st.write("Let's look at raw data in the Pandas Data Frame.")

st.write(df)



# st.write("Hmm 🤔, is there some correlation between body mass and flipper length? Let's make a scatterplot with [Altair](https://altair-viz.github.io/) to find.")

# chart = alt.Chart(df).mark_point().encode(
#     x=alt.X("body_mass_g", scale=alt.Scale(zero=False)),
#     y=alt.Y("flipper_length_mm", scale=alt.Scale(zero=False)),
#     color=alt.Y("species")
# ).properties(
#     width=600, height=400
# ).interactive()

# st.write(chart)

selection = alt.selection_multi(fields=['primary_type'])

chart3 = alt.Chart(df, height=600).mark_area().encode(
    alt.X("year:O"),
    alt.Y("num_crimes:Q", stack='center', axis=None),
    alt.Color("primary_type:N", scale=alt.Scale(scheme='category20b')),
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
    color=alt.Color('primary_type:N', scale=alt.Scale(scheme='category20b'))
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


#crime_url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json?$select=district,count(district),sum(case(arrest='1',1,true,0))&$group=district"
#return pd.read_json(crime_url)

highlight = alt.selection(type='single', on='mouseover', fields=['primary_type'], nearest=True)

crimes_base = alt.Chart(df).encode(
    alt.X('year:O'),
    alt.Y('num_crimes:Q'),
    alt.Color('primary_type:N'),
    tooltip='primary_type:N'
)

crimes_points = crimes_base.mark_circle().encode(
    opacity=alt.value(0)
).add_selection(
    highlight
).properties(
    width=600
)

crimes_lines = crimes_base.mark_line().encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(3)),
    opacity=alt.condition(highlight, alt.value(1), alt.value(0.3))
)

arrests_base = alt.Chart(df).encode(
    alt.X('year:O'),
    alt.Y('arrest_rate:Q'),
    alt.Color('primary_type:N'),
    tooltip='primary_type:N'
)

arrests_points = arrests_base.mark_circle().encode(
    opacity=alt.value(0)
).add_selection(
    highlight
).properties(
    width=600
)

arrests_lines = arrests_base.mark_line().encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(3)),
    opacity=alt.condition(highlight, alt.value(1), alt.value(0.1))
)

st.write(crimes_points+crimes_lines | arrests_points+arrests_lines)

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

st.write(chart2)


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

st.write(coordinate_df)

brush = alt.selection(type='interval')

year_slider = alt.binding_range(min=2001, max=2020, step=1)
slider_selection = alt.selection_single(bind=year_slider, fields=['Release_Year'], name="Release Year_")

location_chart = alt.Chart(coordinate_df).mark_point().encode(
    alt.X('x_coordinate:Q', scale=alt.Scale(zero=False)),
    alt.Y('y_coordinate:Q', scale=alt.Scale(zero=False))
).add_selection(brush)

count_chart = alt.Chart(coordinate_df).mark_bar().encode(
    alt.X('x_coordinate:Q'),
    alt.Y('sum(freq)')
).transform_filter(brush)

st.write(location_chart | count_chart)