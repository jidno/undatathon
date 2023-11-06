import streamlit as st
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

import xgboost as xgb
from sklearn.preprocessing import StandardScaler

model = xgb.XGBRegressor(tree_method="hist", device="cpu")
model.load_model("data/god_model.model")

st.set_page_config(layout="wide")

COUNTRIES_COORDINATES = json.load(open("data/country-by-geo-cordinations_dict.json"))
DATAPOINTS = pd.read_csv("data/datapoints.csv")

st.title("Coping strategy prediction by context")

st.subheader("Context")
country = st.selectbox("Select a country", DATAPOINTS["adm0_name"].unique())
if country:
    regions = DATAPOINTS[DATAPOINTS["adm0_name"] == country]["adm1_name"].unique()
    region = st.selectbox(
        "Select a region", regions, index=regions.tolist().index(regions[0])
    )

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

    if region:
        rounds = DATAPOINTS[
            (DATAPOINTS["adm0_name"] == country) & (DATAPOINTS["adm1_name"] == region)
        ]["inter_round"].unique()
        round = st.selectbox(
            "Select a round", rounds, index=rounds.tolist().index(rounds[0])
        )


columns = DATAPOINTS.columns
fcs_inputs = []
shocks = []
cs = []
for col in columns:
    if col.startswith("fcs_"):
        fcs_inputs.append(col)
    elif col.startswith("shock"):
        shocks.append(col)
    elif col.startswith("cs"):
        cs.append(col)
datapoint = DATAPOINTS[
    (DATAPOINTS["adm0_name"] == country)
    & (DATAPOINTS["adm1_name"] == region)
    & (DATAPOINTS["inter_round"] == round)
]
inputs = {}

st.subheader("Food consumption scores' modification")
st.write("Modify the food consumption scores' values for the selected context")
# st.write("fcs: Food Consumption Score")
# st.write(
#     "fcs_staple_days: How many days over the last 7 days, did members of your household eat starches, roots and tubers such as rice, maize, pasta, bread, sorghum, millet, potato, yam, cassava, white sweet potato?"
# )
# st.write(
#     "fcs_pulses_days: How many days over the last 7 days, did members of your household eat pulses and nuts such as beans, lentils, cowpeas, soybean, pigeon peas and peanuts or other nuts?"
# )
# st.write(
#     "fcs_vegetables_days: How many days over the last 7 days, did members of your household eat vegetables or leaves such as local vegetables and/or other leaves/vegetables?"
# )
# st.write(
#     "fcs_fruit_days: How many days over the last 7 days, did members of your household eat fruit such as local fruits and/or other fruits?"
# )
# st.write(
#     "fcs_meat_fish_days: How many days over the last 7 days, did members of your household eat meat, eggs or fish (any type of meat or fish including insects, birds, bush meat, seafood, or organs)?"
# )
# st.write(
#     "fcs_dairy_days: How many days over the last 7 days, did members of your household eat dairy products such as milk, cheese, yogurt, or butter?"
# )
# st.write(
#     "fcs_sugar_days: How many days over the last 7 days, did members of your household eat sugar, honey, jam, syrup, or chocolate?"
# )
# st.write(
#     "fcs_oil_days: How many days over the last 7 days, did members of your household eat oil, butter, ghee, or margarine?"
# )
# st.write(
#     "fcs_condiments_days: How many days over the last 7 days, did members of your household eat spices or condiments such as tea, coffee, cocoa, salt, garlic, spices, yeast, meat fish as a condiment or small amounts of milk for tea or coffee?"
# )


c1, c2, c3, c4, c5 = st.columns(5)
columns = [c1, c2, c3, c4, c5]

# Next to each of the fcs, add a slider to modify the value

for i, fcs in enumerate(fcs_inputs):
    round_value = datapoint[fcs].values[0]
    if round_value < 0:
        round_value = 0.0
    elif round_value > 7:
        round_value = 7.0
    with columns[i % 5]:
        inputs[fcs] = st.slider(
            label=fcs, min_value=0.0, max_value=7.0, value=round_value
        )

inter_column = st.columns(1)
nc1, nc2, nc3, nc4, nc5 = st.columns(5)
new_columns = [nc1, nc2, nc3, nc4, nc5]
new_value = {}


with inter_column[0]:
    st.subheader("Shocks experimented in simulation context")
    st.write("Modify percentage of the population that experimented each shock")

    # Next to each of the shocks, add a slider to modify the value

    for i, shock in enumerate(shocks):
        with new_columns[i % 5]:
            inputs[shock] = st.slider(
                label=shock, min_value=0.0, max_value=1.0, value=0.0
            )

inter_column = st.columns(1)
simulate_button = st.button("Simulate new coping strategies")
new_coping_strategies = {}

if simulate_button:
    with inter_column[0]:
        st.subheader("Simulation of coping strategies")
        st.write("Predict coping strategies for the modified context")
        sc = StandardScaler()
        inputs_columns = list(inputs.keys())
        sc.fit(DATAPOINTS[inputs_columns])
        inputs = np.array(list(inputs.values()))
        inputs = inputs.reshape(1, -1)
        predictions = model.predict(sc.transform(inputs)).clip(0, 1)
        pred_dict = {"cs": cs, "percentage": predictions.tolist()[0]}
        df = pd.DataFrame(pred_dict)
        st.write(df)

        # Create the bar chart
        st.bar_chart(
            df.set_index("cs")["percentage"],
        )
