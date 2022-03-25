
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

def FreshValDf():    
    t = pd.read_csv('../../data/skyserver_querying/final_combined.csv', skiprows=1)
    
    cols = t.columns.to_numpy()
    # ['name', 'objID', 'ra', 'dec', 'run', 'rerun', 'camcol', 'field','type', ...
    
    # drop 'name' per artifact of query
    t = t.drop('name', axis=1)
    
    cols = t.columns.to_numpy()
    # ['objID', 'ra', 'dec', 'run', 'rerun', 'camcol', 'field','type', 'modelMag_u', 'modelMag_g', 'modelMag_r', 'modelMag_i', 'modelMag_z', 'specObjID', 'plate', 'mjd', 'fiberID']
    
    len(t.specObjID.unique())
    #126598
    
    t.shape
    #(128429, 19)
    
    t.shape[0] - len(t.specObjID.unique())
    #1831
    
    val_cnts = t.specObjID.value_counts()
    val_cnts.reset_index().iloc[0]
    # index        specObjID
    # specObjID            9
    
    #remove header rows (from joining queries)
    rows_to_drop_idx = t[t['specObjID']=='specObjID'].index
    t = t.drop(rows_to_drop_idx)
    
    #check ref and val data for matching spec_obj_IDs
    
    # all duplicated specObjID rows have sames values in all columns
    t.duplicated().sum()
    # 1823 (doesn't include first occurrence)
    len(t) - t.duplicated().sum()
    # 128420 - 1823 = 126597

    t = t.drop(t.loc[t.duplicated()].index)

    len(t)
    # 126597
    len(t['specObjID'].unique())
    # 126597
    return t


tdf = FreshValDf()


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

#%% match up
def ConvertToMatchRef(d):
    d['redshift'] = d['z']
    d['class'] = d['type']
    d['spec_obj_ID'] = d['specObjID']
    d['obj_ID'] = d['objID']
    d['alpha'] = d['ra'].astype(float)
    d['delta'] = d['dec'].astype(float)
    d['u'] = d['modelMag_u'].astype(float)
    d['g'] = d['modelMag_g'].astype(float)
    d['r'] = d['modelMag_r'].astype(float)
    d['i'] = d['modelMag_i'].astype(float)
    d['z'] = d['modelMag_z'].astype(float)
    
    
    d = d.drop(['type'], axis=1)
    d = d.drop(['ra'], axis=1)
    d = d.drop(['dec'], axis=1)
    d = d.drop(['modelMag_u'], axis=1)
    d = d.drop(['modelMag_g'], axis=1)
    d = d.drop(['modelMag_r'], axis=1)
    d = d.drop(['modelMag_i'], axis=1)
    d = d.drop(['modelMag_z'], axis=1)
    
    d['run_ID'] = d['run'].astype(int)
    d['rerun_ID'] = d['rerun'].astype(int)
    d['cam_col'] = d['camcol'].astype(int)
    d['field_ID'] = d['field'].astype(int)
    d['plate'] = d['plate'].astype(int)
    d['MJD'] = d['mjd'].astype(int)
    d['fiber_ID'] = d['fiberID'].astype(int)
    
    d = d.drop(['objID','specObjID', 'run', 
                'rerun', 'camcol', 'field', 
                'mjd', 'fiberID'], axis=1)
    return d
    
#%%
df_val_subset = ConvertToMatchRef(df_val_subset)

#%% check
prnt(df_val_subset)
prnt(df_ref_subset)
print(df_val_subset.shape)
print(df_ref_subset.shape)

#%% write
df_val_subset.to_csv('final_combined_clean_subset_matching_ref.csv')



#%% NO QUASARS?
df_val_subset['class'].value_counts()


#%%
print(df['class'].value_counts())

#%% YUP, NO QUASARS!

df_val = FreshValDf()
df_val['type'].value_counts()
df_val = df_val.drop(df_val[df_val.isna().any(axis=1)].index)
ddd = ConvertToMatchRef(df_val)
prnt(ddd)
print(ddd['class'].value_counts())

t = pd.read_csv('../../data/skyserver_querying/final_combined.csv', skiprows=1)
t['type'].value_counts()
