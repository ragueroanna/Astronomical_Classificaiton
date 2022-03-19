#%% Imports

import numpy as np
import pandas as pd

from os import chdir

#%% working directory

#folder containing repo root
repo_path = r'C:\Users\Bob\Desktop\U\comp5360_final'
#repo_path = r'/Users/roannarague/Documents/BMI_6106_Final'

chdir(repo_path)

chdir('.\EDA\Python')

#%% read in data

df = pd.read_csv('../../data/star_classification.csv')

#%% Fields/Question

df.shape

df.head()

column_names = [x for x in df.columns.values]
categories = df['class'].value_counts().index.values

cats=','.join(categories)
fields=','.join(column_names)
print(f'What is the observation? ({cats})')
print()
print('Predict value of class based on fields:', \
      fields.replace(',class','').replace(',',', '))

#%% EDA
df
#conda create --name astro_env
#conda activate astro_env
#conda install astropy
import astropy
from astropy.io import fits
from astropy.table import Table

#%%
with fits.open('spec-10000-57346-0001.fits') as hdul:
    print(hdul.info())
    print(hdul[1].header)
    print(hdul[1].data)
    # asn_table = Table(hdul[1].data)
    # print(hdul[2].header)
    # print(hdul[2].data)

# print(asn_table)

#%%
# from astropy.wcs import WCS
# import matplotlib.pyplot as plt

#%%
# with fits.open('spec-10000-57346-0001.fits') as hdu:
#     wcs = WCS(fobj=hdu[1], header=hdu[1].header)
    
#%%
#      y1:y2,     x1:x2
# data[2290:2690, 280:680]
#
# .... investigate web scraping or api/query




