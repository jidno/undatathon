# %%
import start  # noqa
import antigranular as ag
import pandas as pd

session = ag.login(
    "dGASFUTW8jVk+lnZ1P8FPzKTn/nFQqq/",
    "WnA3xZ/q9mmEsCd59hscwKhP2Fl2ZvVz78bPPpALz+DJW1ojCpXjCKpoLvAVMBUd",
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

columns_names = undata_cs.columns
columns_names = columns_names.drop("objectid")
for column_name in columns_names:
    undata_cs[f"{column_name}_yes"] = ((undata_cs[column_name] == 1.0) | (undata_cs[column_name] == 3.0)) * 1.0


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

#setup a privacy 
privacy = op_snsql.Privacy(epsilon=0.01 , delta=0.0001)
reader = op_snsql.from_df(df=undata_fcs_adm_other_cs_shock, privacy=privacy)
# %%
%%ag


query = ("SELECT "
         "AVG(fcs) as fcs, "
         "AVG(fcs_staple_days) as fcs_staple_days, "
         "AVG(fcs_pulses_days) as fcs_pulses_days, "
         "AVG(fcs_vegetables_days) as fcs_vegetables_days, "
         "AVG(fcs_fruit_days) as fcs_fruit_days, "
         "AVG(fcs_meat_fish_days) as fcs_meat_fish_days, "
         "AVG(fcs_dairy_days) as fcs_dairy_days, "
         "AVG(fcs_sugar_days) as fcs_sugar_days, "
         "AVG(fcs_oil_days) as fcs_oil_days, "
         "AVG(fcs_condiments_days) as fcs_condiments_days, "
         "AVG(shock_noshock) as shock_noshock, "
         "AVG(shock_sicknessordeathofhh) as shock_sicknessordeathofhh, "
         "AVG(shock_lostemplorwork) as shock_lostemplorwork, "
         "AVG(shock_otherintrahhshock) as shock_otherintrahhshock, "
         "AVG(shock_higherfoodprices) as shock_higherfoodprices, "
         "AVG(shock_higherfuelprices) as shock_higherfuelprices, "
         "AVG(shock_mvtrestrict) as shock_mvtrestrict, "
         "AVG(shock_othereconomicshock) as shock_othereconomicshock, "
         "AVG(shock_pestoutbreak) as shock_pestoutbreak, "
         "AVG(shock_plantdisease) as shock_plantdisease, "
         "AVG(shock_animaldisease) as shock_animaldisease, "
         "AVG(shock_napasture) as shock_napasture, "
         "AVG(shock_othercropandlivests) as shock_othercropandlivests, "
         "AVG(shock_coldtemporhail) as shock_coldtemporhail, "
         "AVG(shock_flood) as shock_flood, "
         "AVG(shock_hurricane) as shock_hurricane, "
         "AVG(shock_drought) as shock_drought, "
         "AVG(shock_earthquake) as shock_earthquake, "
         "AVG(shock_landslides) as shock_landslides, "
         "AVG(shock_firenatural) as shock_firenatural, "
         "AVG(shock_othernathazard) as shock_othernathazard, "
         "AVG(shock_violenceinsecconf) as shock_violenceinsecconf, "
         "AVG(shock_theftofprodassets) as shock_theftofprodassets, "
         "AVG(shock_firemanmade) as shock_firemanmade, "
         "AVG(shock_othermanmadehazard) as shock_othermanmadehazard, "
        #  "AVG(cs_hh_assets_yes) as cs_hh_assets_yes, "
        #  "AVG(cs_spent_savings_yes) as cs_spent_savings_yes, "
         "AVG(cs_sold_more_animals_yes) as cs_sold_more_animals_yes, "
        #  "AVG(cs_eat_elsewhere_yes) as cs_eat_elsewhere_yes, "
        #  "AVG(cs_borrowed_or_helped_yes) as cs_borrowed_or_helped_yes, "
        #  "AVG(cs_credit_yes) as cs_credit_yes, "
         "AVG(cs_borrowed_money_yes) as cs_borrowed_money_yes, "
        #  "AVG(cs_changed_school_yes) as cs_changed_school_yes, "
         "AVG(cs_sold_prod_assets_yes) as cs_sold_prod_assets_yes, "
        #  "AVG(cs_no_school_yes) as cs_no_school_yes, "
        #  "AVG(cs_reduced_health_exp_yes) as cs_reduced_health_exp_yes, "
        #  "AVG(cs_harv_immature_crops_yes) as cs_harv_immature_crops_yes, "
        #  "AVG(cs_consume_seed_stock_yes) as cs_consume_seed_stock_yes, "
        #  "AVG(cs_decrease_input_exp_yes) as cs_decrease_input_exp_yes, "
        #  "AVG(cs_sold_house_yes) as cs_sold_house_yes, "
         "AVG(cs_begged_yes) as cs_begged_yes, "
        #  "AVG(cs_illegal_yes) as cs_illegal_yes, "
        #  "AVG(cs_sold_last_female_yes) as cs_sold_last_female_yes, "
        #  "AVG(cs_hh_migration_yes) as cs_hh_migration_yes, "
         "adm0_m49, "
         "inter_round "
         "from df.table "
         "WHERE shock_dk = 0.0 AND shock_ref = 0.0 "
         "GROUP BY adm0_m49, inter_round"
)
total_cost = reader.get_privacy_cost(
    [query]
)
export(str(total_cost) , "total_cost")
# %%
print(total_cost) # (epsilon , delta)
# %%
%%ag

res = reader.execute(query)
export(str(res), "res")
# %%
import ast
res_list = ast.literal_eval(res)
res_list
# %%
# open jack.txt
saved_res_txt = open("saved_res.txt", "r").read()
saved_res = ast.literal_eval(saved_res_txt)
res_list = saved_res
res_list
# %%
# column_names = ["fcs", "fcs_staple_days", "fcs_pulses_days", "fcs_vegetables_days", "adm1_pcode", "inter_round"]
column_names, res_values = res_list[0], res_list[1:]
res_df = pd.DataFrame(res_values, columns=column_names)
res_df
# %%
# save to csv
res_df.to_csv("res_df.csv")
# %