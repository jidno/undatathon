# %%
import start  # noqa
import antigranular as ag
import pandas as pd
import numpy as np

session = ag.login(
    "jF5mrZjKiL0y0H4XNRrXvc+S1Ius5Wv0",
    "Sf44gkSvMROSBIAwmxk9CX02LxMwJdb+UsGpHuukxs4AqsY0rFHNWCtGt3i58T/W",
    competition="UN Datathon PETs Track",
)
# %%
session.privacy_odometer()
# %%
%%ag

undata_fcs = load_dataset("undata_fcs")
undata_adm = load_dataset("undata_adm")
undata_other = load_dataset("undata_other")
undata_cs = load_dataset("undata_cs")
undata_shock= load_dataset("undata_shock")

# Drop all rows on undata_cs where the value in not 0, 1, 2 or 3
# from all columns except objectid


undata_fcs_adm = undata_fcs.join(undata_adm, on="objectid", how="inner", rsuffix="_adm")
undata_fcs_adm_other = undata_fcs_adm.join(
    undata_other, on="objectid", how="inner", rsuffix="_other"
)
undata_fcs_adm_other["inter_round"] = undata_fcs_adm_other["round"]
undata_fcs_adm_other_cs = undata_fcs_adm_other.join(
    undata_cs, on="objectid", how="inner", rsuffix="_cs"
)
undata_fcs_adm_other_cs_shock = undata_fcs_adm_other_cs.join(
    undata_shock, on="objectid", how="inner", rsuffix="_shock"
)

# Drop all 

ag_print("Details: \n")
ag_print("Columns: \n", undata_fcs_adm_other_cs_shock.columns)
ag_print("Metadata: \n", undata_fcs_adm_other_cs_shock.metadata)
ag_print("Dtypes: \n", undata_fcs_adm_other_cs_shock.dtypes)
# %%
%%ag
import op_snsql

#setup a privacy l
privacy = op_snsql.Privacy(epsilon=0.1 , delta=0.01)
reader = op_snsql.from_df(df=undata_fcs_adm_other, privacy=privacy)
# %%
%%ag

query = ("SELECT "
         "AVG(fcs), "
         "AVG(fcs_staple_days), "
         "AVG(fcs_pulses_days), "
         "AVG(fcs_vegetables_days), "
         "adm1_pcode, "
         "inter_round "
         "from df.table "
         "GROUP BY adm1_pcode, inter_round")
total_cost = reader.get_privacy_cost(
    [query]
)
export(str(total_cost) , "total_cost")
# %%
print(total_cost) # (epsilon , delta)
# %%
%%ag

res = reader.execute(query)
export(res, "res")
# %%
res
# %%
column_names = ["fcs", "fcs_staple_days", "fcs_pulses_days", "fcs_vegetables_days", "adm1_pcode", "inter_round"]
res_df = pd.DataFrame(res[1:], columns=column_names)
res_df
# %%
# save to csv
res_df.to_csv("res_df2.csv")
# %%

query = ("SELECT "
         "AVG(fcs) as fcs, "
         "AVG(fcs_staple_days) as fcs_staple_days, "
         "AVG(fcs_pulses_days) as fcs_pulses_days, "
         "AVG(fcs_vegetables_days) as fcs_vegetables_days, "
         "COUNT(shock_noshock) as shock_noshock, "
         "COUNT(shock_sicknessordeathofhh) as shock_sicknessordeathofhh, "
         "COUNT(shock_lostemplorwork) as shock_lostemplorwork, "
         "COUNT(shock_otherintrahhshock) as shock_otherintrahhshock, "
         "COUNT(shock_higherfoodprices) as shock_higherfoodprices, "
         "COUNT(shock_higherfuelprices) as shock_higherfuelprices, "
         "COUNT(shock_mvtrestrict) as shock_mvtrestrict, "
         "COUNT(shock_othereconomicshock) as shock_othereconomicshock, "
         "COUNT(shock_pestoutbreak) as shock_pestoutbreak, "
         "COUNT(shock_plantdisease) as shock_plantdisease, "
         "COUNT(shock_animaldisease) as shock_animaldisease, "
         "COUNT(shock_napasture) as shock_napasture, "
         "COUNT(shock_othercropandlivests) as shock_othercropandlivests, "
         "COUNT(shock_coldtemporhail) as shock_coldtemporhail, "
         "COUNT(shock_flood) as shock_flood, "
         "COUNT(shock_hurricane) as shock_hurricane, "
         "COUNT(shock_drought) as shock_drought, "
         "COUNT(shock_earthquake) as shock_earthquake, "
         "COUNT(shock_landslides) as shock_landslides, "
         "COUNT(shock_firenatural) as shock_firenatural, "
         "COUNT(shock_othernathazard) as shock_othernathazard, "
         "COUNT(shock_violenceinsecconf) as shock_violenceinsecconf, "
         "COUNT(shock_theftofprodassets) as shock_theftofprodassets, "
         "COUNT(shock_firemanmade) as shock_firemanmade, "
         "COUNT(shock_othermanmadehazard) as shock_othermanmadehazard, "
         "adm1_pcode, "
         "inter_round "
         "from df.table "
         "WHERE shock_dk = 0.0 AND shock_ref = 0.0 "
         "GROUP BY adm1_pcode, inter_round"
)
query
# %%
