
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


#%%% build 
out_dir = '../../data/skyserver_querying'

num_chunks = 10
num_objs = df.shape[0]
chunk_size = int(num_objs / num_chunks)

for i in range(num_chunks):    
    ra_dec = []
    ra_dec.append('  name  ra         dec\n')
    idx = 0
    start = chunk_size * i
    end = start + chunk_size - 1
    if num_chunks == i + 1:
        end += 1
    for ids in df.loc[start:end,['alpha', 'delta']].values:
        idx += 1
        xname = hex(idx)[2:]
        ra_dec.append(f'  {xname:<4}  {ids[0]:<19}  {ids[1]}\n')        
    
    with open(f'{out_dir}/ra_dec_{start}-{end}.txt','w') as f:
        f.writelines(ra_dec)


