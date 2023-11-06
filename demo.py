import streamlit as st
import pandas as pd
import numpy as np
import json

COUNTRIES_COORDINATES = json.load(open("country-by-geo-cordinations_dict.json"))

st.title("Coping strategy prediction by context")

st.subheader("Context")
country = st.selectbox("Select a country", COUNTRIES_COORDINATES.keys())

coordinates = COUNTRIES_COORDINATES[country]
df = pd.DataFrame(
    {
        "col1": [float(coordinates["north"]), float(coordinates["south"])],
        "col2": [float(coordinates["east"]), float(coordinates["west"])],
    }
)
st.map(
    df,
    latitude="col1",
    longitude="col2",
    color=[0, 0, 0, 0],
)

st.subheader("Main indicators")
coping_strategies = {
    "Uruguay": {
        "cs1": {"0-25": 30, "25-50": 30, "50-75": 30, "75-100": 10},
        "cs2": {"0-25": 40, "25-50": 30, "50-75": 20, "75-100": 10},
    },
    "Brazil": {
        "cs1": {"0-25": 20, "25-50": 30, "50-75": 40, "75-100": 10},
        "cs2": {"0-25": 10, "25-50": 30, "50-75": 20, "75-100": 40},
    },
}

fcs = {
    "fcs": "Food Consumption Score",
    "fcs_staple_days": "How many days over the last 7 days, did members of your household eat starches, roots and tubers such as rice, maize, pasta, bread, sorghum, millet, potato, yam, cassava, white sweet potato?",
    "fcs_pulses_days": "How many days over the last 7 days, did members of your household eat pulses and nuts such as beans, lentils, cowpeas, soybean, pigeon peas and peanuts or other nuts?",
    "fcs_vegetables_days": "How many days over the last 7 days, did members of your household eat vegetables or leaves such as local vegetables and/or other leaves/vegetables?",
    "fcs_fruit_days": "How many days over the last 7 days, did members of your household eat fruit such as local fruits and/or other fruits?",
    "fcs_meat_fish_days": "How many days over the last 7 days, did members of your household eat meat, eggs or fish (any type of meat or fish including insects, birds, bush meat, seafood, or organs)?",
    "fcs_dairy_days": "How many days over the last 7 days, did members of your household eat dairy products such as milk, cheese, yogurt, or butter?",
    "fcs_sugar_days": "How many days over the last 7 days, did members of your household eat sugar, honey, jam, syrup, or chocolate?",
    "fcs_oil_days": "How many days over the last 7 days, did members of your household eat oil, butter, ghee, or margarine?",
    "fcs_condiments_days": "How many days over the last 7 days, did members of your household eat spices or condiments such as tea, coffee, cocoa, salt, garlic, spices, yeast, meat fish as a condiment or small amounts of milk for tea or coffee?",
}

cs = 


indicators = {
    "Uruguay": {
        "FCS": 1000,
        "Population": 1000000,
        "Population density": 100,
        "Urban population": 1000000,
        "Rural population": 1000000,
        "Gini coefficient": 0.5,
    },
    "Brazil": {
        "GDP per capita": 9999,
        "Population": 9999000,
        "Population density": 100,
        "Urban population": 9999000,
        "Rural population": 9999000,
        "Gini coefficient": 0.9,
    },
}

c1, c2, c3, c4, c5 = st.columns(5)
columns = [c1, c2, c3, c4, c5]

# Next to each of the indicators, write the value of the indicator and add a button to
# add or subtract 1 from the value of the indicator.

percentage_change = np.zeros(len(indicators[country]))
for i, (indicator, value) in enumerate(indicators[country].items()):
    with columns[i % 5]:
        st.write(indicator)
        st.write(value)
        percentage_change[i] = st.number_input(
            label="Percentage change", value=0, key=i
        )

inter_column = st.columns(1)
calculate_button = st.button("Calculate new values")
nc1, nc2, nc3, nc4, nc5 = st.columns(5)
new_columns = [nc1, nc2, nc3, nc4, nc5]
new_value = {}

if calculate_button:
    with inter_column[0]:
        st.subheader("Simulation context")
        for i, (indicator, value) in enumerate(indicators[country].items()):
            with new_columns[i % 5]:
                new_value[indicator] = value * (1 + percentage_change[i] / 100)

                st.write(indicator)
                st.write(new_value[indicator])

inter_column = st.columns(1)
simulate_button = st.button("Simulate new coping strategies")
cs1, cs2 = st.columns(2)
new_coping_strategies = {}

if simulate_button:
    with inter_column[0]:
        st.subheader("Simulation coping strategies")
        with cs1:
            cs_dfs = {}

            for coping_strategy in coping_strategies[country]:
                cs_dfs[coping_strategy] = pd.DataFrame(
                    coping_strategies[country][coping_strategy], index=[coping_strategy]
                )

            df = pd.concat(cs_dfs, axis=0)
            df = df.drop(df.columns[0], axis=1)
            st.write(cs_dfs["cs1"])
            st.write(df)
st.subheader("Coping strategies prediction")
