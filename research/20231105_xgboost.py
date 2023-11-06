#%%
import xgboost as xgb
model = xgb.XGBRegressor(tree_method="hist", device="cpu")
model.load_model("/home/catalina/workspace/undatathon/data/god_model_2.model")

#%%
import pandas as pd
from sklearn.preprocessing import StandardScaler


X_train = pd.read_csv("/home/catalina/workspace/undatathon/data/jack_df.csv")
#%%

X_train = X_train[["fcs",'fcs_staple_days', 'fcs_pulses_days', 'fcs_vegetables_days',
    'fcs_fruit_days', 'fcs_meat_fish_days', 'fcs_dairy_days',
    'fcs_sugar_days', 'fcs_oil_days', 'fcs_condiments_days',
    'shock_noshock', 'shock_sicknessordeathofhh', 'shock_lostemplorwork',
    'shock_otherintrahhshock', 'shock_higherfoodprices',
    'shock_higherfuelprices', 'shock_mvtrestrict',
    'shock_othereconomicshock', 'shock_pestoutbreak', 'shock_plantdisease',
    'shock_animaldisease', 'shock_napasture', 'shock_othercropandlivests',
    'shock_coldtemporhail', 'shock_flood', 'shock_hurricane',
    'shock_drought', 'shock_earthquake', 'shock_landslides',
    'shock_firenatural', 'shock_othernathazard', 'shock_violenceinsecconf',
    'shock_theftofprodassets', 'shock_firemanmade',
    'shock_othermanmadehazard']]


#%%
sc = StandardScaler()
sc.fit(X_train)

X_train_transformed = sc.transform(X_train)
#%%

example = sc.transform(X_train.iloc[0].to_numpy().reshape(1, -1))
example
#%%
model.predict(example)
# %%
df = pd.read_csv("/home/catalina/workspace/undatathon/data/jack_df.csv")
Y_train = df[df.columns[-6:-2]]
# %%
Y_train.iloc[0]