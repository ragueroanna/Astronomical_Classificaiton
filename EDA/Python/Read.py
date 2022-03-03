#%% Imports

import numpy as np
import pandas as pd

from os import chdir

#%% working directory

#folder containing repo root
repo_path = r'C:\Users\Bob\Desktop\U\comp5360_final'
#repo_path = r'C:\Users\roannarague\Documents\BMI_6106_Final'

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

#TODO