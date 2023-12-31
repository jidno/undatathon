# # %%
# # import start  # noqa
# import json

# json_path = "/home/frei/workspace/undatathon/country-by-geo-cordinations.json"
# COUNTRIES_COORDINATES = json.load(open(json_path))

# # %%
# # Create new dict from COUNTRIES_COORDINATES to have as keys the country names, and as values the coordinates
# COUNTRIES_COORDINATES_DICT = {}
# for country in COUNTRIES_COORDINATES:
#     COUNTRIES_COORDINATES_DICT[country["country"]] = country
#     # Delete the country key from the dict
#     del COUNTRIES_COORDINATES_DICT[country["country"]]["country"]

# COUNTRIES_COORDINATES_DICT
# # %%
# # Save json file
# with open("country-by-geo-cordinations_dict.json", "w") as outfile:
#     json.dump(COUNTRIES_COORDINATES_DICT, outfile)

# # %%
# # Load json file
# COUNTRIES_COORDINATES_DICT = json.load(
#     open("/home/frei/workspace/undatathon/country-by-geo-cordinations_dict.json")
# )
# COUNTRIES_COORDINATES_DICT

# # %%
# import pandas as pd

# country = "Uruguay"

# coping_strategies = {
#     "Uruguay": {
#         "cs1": {"0-25": 30, "25-50": 30, "50-75": 30, "75-100": 10},
#         "cs2": {"0-25": 40, "25-50": 30, "50-75": 20, "75-100": 10},
#     },
#     "Brazil": {
#         "cs1": {"0-25": 20, "25-50": 30, "50-75": 40, "75-100": 10},
#         "cs2": {"0-25": 10, "25-50": 30, "50-75": 20, "75-100": 40},
#     },
# }
# cs_dfs = {}
# for coping_strategy in coping_strategies[country]:
#     cs_dfs[coping_strategy] = pd.DataFrame(
#         coping_strategies[country][coping_strategy], index=[0]
#     )

# df = pd.concat(cs_dfs, axis=0)
# df.head()

# # coping_data = pd.DataFrame(coping_strategies[country], index=[0])
# # coping_data.head()
# # coping_strategies[country][coping_strategy]

# %%
import xgboost as xgb
model = xgb.XGBRegressor(tree_method="hist", device="cpu")
model.load_model("god_model.model")
model.predict(X)

# X: ['fcs', 'fcs_staple_days', 'fcs_pulses_days', 'fcs_vegetables_days',
      #  'fcs_fruit_days', 'fcs_meat_fish_days', 'fcs_dairy_days',
      #  'fcs_sugar_days', 'fcs_oil_days', 'fcs_condiments_days',
      #  'shock_noshock', 'shock_sicknessordeathofhh', 'shock_lostemplorwork',
      #  'shock_otherintrahhshock', 'shock_higherfoodprices',
      #  'shock_higherfuelprices', 'shock_mvtrestrict',
      #  'shock_othereconomicshock', 'shock_pestoutbreak', 'shock_plantdisease',
      #  'shock_animaldisease', 'shock_napasture', 'shock_othercropandlivests',
      #  'shock_coldtemporhail', 'shock_flood', 'shock_hurricane',
      #  'shock_drought', 'shock_earthquake', 'shock_landslides',
      #  'shock_firenatural', 'shock_othernathazard', 'shock_violenceinsecconf',
      #  'shock_theftofprodassets', 'shock_firemanmade',
      #  'shock_othermanmadehazard']

#%%
Metricas Train (MSE):

cs_sold_more_animals_yes    2.892967e-07
cs_borrowed_money_yes       3.036846e-07
cs_sold_prod_assets_yes     2.460369e-07
cs_begged_yes               2.996433e-07

cs_sold_more_animals_yes    0.275278
cs_borrowed_money_yes       0.332863
cs_sold_prod_assets_yes     0.333548
cs_begged_yes               0.087751
# %%
import pandas as pd


datapoints = pd.read_csv("/home/frei/workspace/undatathon/jack_df.csv")
datapoints
# %%
import start
import pandas as pd

# %%
jack_df = pd.read_csv("data/jack_df.csv")
adm_level = pd.read_csv("data/level_1.csv")

# %%
jack_df
# %%
adm_level = adm_level[["adm1_name", "adm1_pcode", "adm0_name"]]
# %%
adm_level
# %%
jack_df = jack_df.merge(adm_level, on="adm1_pcode", how="inner")

# %%
jack_df
# %%
# Save to datapoints.csv
jack_df.to_csv("datapoints.csv", index=False)
# %%
datapoints = pd.read_csv("datapoints.csv")
datapoints
# %%
columns = datapoints.columns.values.tolist()

# %%
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
         

print(fcs_inputs)
print(shocks)
print(cs)
# %%
countries = datapoints["adm0_name"].unique().tolist()
countries
# %%
country_regions = datapoints[["adm0_name", "adm1_name"]].drop_duplicates()
country_regions
# %%
regions = datapoints["adm1_name"].unique().tolist()
regions

# %%
# Get rounds for a specific country and region
country = "Afghanistan"
region = "Kabul"
rounds = datapoints[(datapoints["adm0_name"] == country) & (datapoints["adm1_name"] == region)]["inter_round"].unique().tolist()


rounds

# %%
