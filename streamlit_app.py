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

#selection = alt.selection_multi(fields=['Primary Type'], bind='legend')

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
