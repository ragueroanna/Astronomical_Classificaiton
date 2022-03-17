
#%% Imports

import numpy as np
import pandas as pd
from os import chdir


#%% working directory

#folder containing repo root
repo_path = r'C:\Users\Bob\Desktop\U\comp5360_final'
#repo_path = r'/Users/roannarague/Documents/BMI_6106_Final'

chdir(repo_path)

chdir('./data_acquisition/Python')


#%% read in reference data

df = pd.read_csv('../../data/star_classification.csv')


#%% clean up join of queries

tdf = pd.read_csv('../../data/skyserver_querying/final_combined.csv', skiprows=1)

cols = tdf.columns.to_numpy()
# ['name', 'objID', 'ra', 'dec', 'run', 'rerun', 'camcol', 'field','type', ...

# drop 'name' per artifact of query
tdf = tdf.drop('name', axis=1)

cols = tdf.columns.to_numpy()
# ['objID', 'ra', 'dec', 'run', 'rerun', 'camcol', 'field','type', 'modelMag_u', 'modelMag_g', 'modelMag_r', 'modelMag_i', 'modelMag_z', 'specObjID', 'plate', 'mjd', 'fiberID']

len(tdf.specObjID.unique())
#126598

tdf.shape
#(128429, 19)

tdf.shape[0] - len(tdf.specObjID.unique())
#1831

val_cnts = tdf.specObjID.value_counts()
val_cnts.reset_index().iloc[0]
# index        specObjID
# specObjID            9

#remove header rows (from joining queries)
rows_to_drop_idx = tdf[tdf['specObjID']=='specObjID'].index
tdf = tdf.drop(rows_to_drop_idx)

#%% check ref and val data for matching spec_obj_IDs

#slow way of checking
#
# val_cnts = tdf.specObjID.value_counts()
# dup_spec_obj_ids = val_cnts[tdf.specObjID.value_counts() > 1].index.to_numpy()

# any_non_duplicates = False
# for dup_spec_obj_id in dup_spec_obj_ids:
#     dups = tdf[tdf['specObjID']==dup_spec_obj_id]
#     for col in cols:
#         if len(dups[col].unique()) > 1:
#             any_non_duplicates = True

# all duplicated specObjID rows have sames values in all columns

tdf.duplicated().sum()
# 1823 (doesn't include first occurrence)
len(tdf) - tdf.duplicated().sum()
# 128420 - 1823 = 126597

tdf = tdf.drop(tdf.loc[tdf.duplicated()].index)

len(tdf)
# 126597
len(tdf['specObjID'].unique())
# 126597

#%% subset ref and val data by matching spec_obj_IDs

ref_spec_obj_ids = df['spec_obj_ID'].to_numpy()
val_spec_obj_ids = tdf['specObjID'].astype(float).to_numpy()

spec_obj_ids_from_val_in_ref = val_spec_obj_ids[np.in1d(val_spec_obj_ids, ref_spec_obj_ids)]
len(spec_obj_ids_from_val_in_ref)
#71155

ref_spec_obj_ids = df['spec_obj_ID'].apply(lambda x: str(int(x))).to_numpy()
val_spec_obj_ids = tdf['specObjID'].to_numpy()

spec_obj_ids_from_val_in_ref = val_spec_obj_ids[np.in1d(val_spec_obj_ids, ref_spec_obj_ids)]
len(spec_obj_ids_from_val_in_ref)
#71155

# subset queried data (common soi w/ref data)
df_val_subset = tdf[tdf['specObjID'].isin(spec_obj_ids_from_val_in_ref)]
df_val_subset.shape

# subset ref data
soi_float = spec_obj_ids_from_val_in_ref.astype(float)
df_ref_subset = df[df['spec_obj_ID'].isin(soi_float)]
df_ref_subset.shape


#%% look at data types/values to decide what makes sense

def prnt(df):
    print()
    idx = df.dtypes.index
    dt = df.dtypes
    val = df.iloc[0]
    for i in range(len(val)):
        typ = str(dt[i])
        print(f'{typ:<10}  {idx[i]:<15}{val[i]:>24}')
    print()
    
prnt(df_ref_subset)
# float64     obj_ID           1.2376609613277432e+18
# float64     alpha                    135.6891066036
# float64     delta                  32.4946318397087
# float64     u                              23.87882
# float64     g                               22.2753
# float64     r                              20.39501
# float64     i                              19.16573
# float64     z                              18.79371
# int64       run_ID                             3606
# int64       rerun_ID                            301
# int64       cam_col                               2
# int64       field_ID                             79
# float64     spec_obj_ID       6.543777369295182e+18
# object      class                            GALAXY
# float64     redshift                      0.6347936
# int64       plate                              5812
# int64       MJD                               56354
# int64       fiber_ID                            171

prnt(df_val_subset)
# object      objID               1237660961327743273
# object      ra                       135.6891066036
# object      dec                    32.4946318397087
# object      run                                3606
# object      rerun                               301
# object      camcol                                2
# object      field                                79
# object      type                             GALAXY
# object      modelMag_u                     23.87882
# object      modelMag_g                      22.2753
# object      modelMag_r                     20.39501
# object      modelMag_i                     19.16573
# object      modelMag_z                     18.79371
# object      specObjID           6543777369295181824
# object      plate                              5812
# object      mjd                               56354
# object      fiberID                             171
# object      z                             0.6347936

#%% WiP
df_val_subset['class'] = df_val_subset['type']
df_val_subset['spec_obj_ID'] = df_val_subset['specObjID']
df_val_subset['alpha'] = df_val_subset['ra'].astype(float)
df_val_subset['delta'] = df_val_subset['dec'].astype(float)
df_val_subset['u'] = df_val_subset['modelMag_u'].astype(float)
df_val_subset['g'] = df_val_subset['modelMag_g'].astype(float)
df_val_subset['r'] = df_val_subset['modelMag_r'].astype(float)
df_val_subset['i'] = df_val_subset['modelMag_i'].astype(float)
df_val_subset['z'] = df_val_subset['modelMag_z'].astype(float)


df_val_subset = df_val_subset.drop(['type'], axis=1)
df_val_subset = df_val_subset.drop(['ra'], axis=1)
df_val_subset = df_val_subset.drop(['dec'], axis=1)
df_val_subset = df_val_subset.drop(['modelMag_u'], axis=1)
df_val_subset = df_val_subset.drop(['modelMag_g'], axis=1)
df_val_subset = df_val_subset.drop(['modelMag_r'], axis=1)
df_val_subset = df_val_subset.drop(['modelMag_i'], axis=1)
df_val_subset = df_val_subset.drop(['modelMag_z'], axis=1)

df_val_subset['run_ID'] = df_val_subset['run'].astype(int)
df_val_subset['rerun_ID'] = df_val_subset['rerun'].astype(int)
df_val_subset['cam_col'] = df_val_subset['camcol'].astype(int)
df_val_subset['field_ID'] = df_val_subset['field'].astype(int)
df_val_subset['plate'] = df_val_subset['plate'].astype(int)
df_val_subset['MJD'] = df_val_subset['mjd'].astype(int)
df_val_subset['fiber_ID'] = df_val_subset['fiberID'].astype(int)


df_val_subset = df_val_subset.drop(['run'], axis=1)
df_val_subset = df_val_subset.drop(['rerun'], axis=1)
df_val_subset = df_val_subset.drop(['camcol'], axis=1)
df_val_subset = df_val_subset.drop(['field'], axis=1)
df_val_subset = df_val_subset.drop(['mjd'], axis=1)
df_val_subset = df_val_subset.drop(['fiberID'], axis=1)
prnt(df_val_subset)
prnt(df_ref_subset)
#%%


