# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 23:53:17 2022

@author: Bob
"""
#%% imports
from bs4 import BeautifulSoup
#import urllib.request
#import re
from selenium import webdriver
import time
from os import listdir
from os import chdir
import pandas as pd




#%% SWITCHES

#folder containing repo root
repo_path = r'C:\Users\Bob\Desktop\U\comp5360_final'
#repo_path = r'/Users/roannarague/Documents/BMI_6106_Final'

#
web_driver_path = 'C:/Users/Bob/Downloads/chromedriver_win32/chromedriver.exe'
#web_driver_path = '/Users/roannarague/Downloads/chromedriver_win32/chromedriver.exe'

# set FALSE for imaging data
#want_optical_spectra = True
want_optical_spectra = False





#%% working directory
chdir(repo_path)
chdir('.\data_acquisition\Python')

#%% data temp/out dirs
web_scraping_dir = '../../data/web_scraping'
data_folder = 'optical_spectra_data' if want_optical_spectra else 'imaging_data'
data_out_dir = f'{web_scraping_dir}/{data_folder}'
temp_html_dir = f'{web_scraping_dir}/temp_html'

#%% out file
data_type = 'optical_spectra' if want_optical_spectra else 'imaging_data'
out_csv = f'{data_out_dir}/{data_type}_first_10000.csv'

#%% read in reference data
df = pd.read_csv('../../data/star_classification.csv')

#%% scrape table from each spec_obj_ID's page in 1 second intervals and write to file
optical_spectra_url = 'http://skyserver.sdss.org/dr17/VisualTools/explore/displayresults?name=SpecObjQuery'
imaging_url = 'https://skyserver.sdss.org/dr17/VisualTools/explore/displayresults?name=PhotoObjQuery'
spec_obj_ID_param = '&spec=' # common parameter
obj_ID_param = '&id=' # imaging parameter

abort = False
no_data = []
with webdriver.Chrome(web_driver_path) as driver:
    for ids in df.loc[0:10000,['spec_obj_ID','obj_ID']].to_numpy():
        specObjId = int(ids[0])
        objId = int(ids[1])
        query = ''
        if want_optical_spectra:
            query = f'{optical_spectra_url}{spec_obj_ID_param}{specObjId}'
        else:
            query = f'{imaging_url}{obj_ID_param}{objId}{spec_obj_ID_param}{specObjId}'
        try:
            driver.get(query)
            table = driver.find_element_by_xpath('//table/..')
            table_html = table.get_attribute('innerHTML')
            with open(f'{temp_html_dir}/{specObjId}.html', 'w') as new_file:
                new_file.write(table_html)
        except:
            no_data.append(specObjId)
        time.sleep(1)
        if not abort:
            continue
        break
    
    
    with open(f'{data_out_dir}/no_data_spec_Obj_Ids_first_10000.txt','w') as nd_file:
        nd_file.write(f'{no_data}')


#%% list all files in saved HTML directory
pages = []
for file in listdir(temp_html_dir):
    with open(f'{temp_html_dir}/{file}', encoding='utf-8') as f:
        pages.append(BeautifulSoup(f.read(), 'html.parser'))


#%% hacky way to visualize first page contents
len(pages)
pg = pages[0]
pg.text.replace('\n',' ').replace('   ',',')[2:3424].replace(' ',': ').split(',') # run line for clean visual


#%% extract key/value pairs from each page into list of dicts
spec_obj_dictionaries = []
pg_idx = 0
for page in pages:
    try:
        pdict = {}
        for row in page.select('tr'):
            field = row.select('tr > th > span')[0].text
            value = row.select('tr > td')[0].text
            if field == 'img':
                break
            pdict[field]=value
        spec_obj_dictionaries.append(pdict)
    except Exception as e:
        print(f'Broke on page index {pg_idx} due to {str(e)}')
    pg_idx += 1

        
#%% check successful scrapes weren't all GALAXY
sdf = pd.DataFrame(spec_obj_dictionaries)
#print(sdf['class'].value_counts()) not all team members' scrape designations have class
#sdf['spec_obj_ID']...

# TODO: RO PR -> df.iloc[0] =>
# obj_ID         1237660961327743232.0
# alpha                     135.689107
# delta                      32.494632
# u                           23.87882
# g                            22.2753
# r                           20.39501
# i                           19.16573
# z                           18.79371
# run_ID                          3606
# rerun_ID                         301
# cam_col                            2
# field_ID                          79
# spec_obj_ID    6543777369295181824.0
# class                         GALAXY
# redshift                    0.634794
# plate                           5812
# MJD                            56354
# fiber_ID                         171

# 6543777369295181824.html written to disk has specObjID of 0
#
# fortunately, the file name has this ID and in memory list of soup, 
# but I am concerned about the values 
# (e.g. 'u'='23.87882' (above) vs sdf.iloc[0].u=='23.78062') 
# in cases where we get this specObjId

#%% save to disk for team merge
sdf.to_csv(out_csv)

#%% check
test = pd.read_csv(out_csv)

