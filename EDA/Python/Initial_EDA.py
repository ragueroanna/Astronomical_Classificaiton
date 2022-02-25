#%% Imports/Data
import numpy as np
import pandas as pd


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
print(f'Predict value of class based on fields: {fields}')

#%% EDA

#TODO