#import collections

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean 

import json

with open('neighborhood.geojson') as f:
    data = json.load(f)
    
neighborhoods_geom = {}
for feature in data['features']:
    neighborhoods_geom[feature['properties']['AFFGEOID']]=feature['geometry']['coordinates'][0][0]


#### AGE ####
age = pd.read_csv('age.csv',skiprows=1)
age = age.drop(0)
age = age[['Id','Both sexes']]
age.columns = ['Id','age']
age = age.reset_index(drop=True)

DROP = age.index[age['age'] == 0].tolist()


#### BEDROOMS ####
bedrooms = pd.read_csv('bedrooms.csv',skiprows=1)
bedrooms = bedrooms.drop(0)
bedrooms['bedrooms'] = bedrooms[['1 bedroom','2 bedrooms','3 bedrooms','4 bedrooms','5 or more bedrooms']].idxmax(axis=1).str[0].astype(np.float64)
bedrooms = bedrooms[['Id','bedrooms']]
bedrooms = bedrooms.reset_index(drop=True)


#### BEDROOMS ####
family_type = pd.read_csv('family_type.csv',header=None)
headers = family_type.iloc[0]
family_type = family_type[3:]
family_type.columns = headers

family_type[['VD03','VD07','VD10','VD14','VD16','VD20']]=family_type[['VD03','VD07','VD10','VD14','VD16','VD20']].astype(np.float64)
family_type = family_type[['GEO.id','VD03','VD07','VD10','VD14','VD16','VD20']]

family_type['type']=family_type[['VD03','VD07','VD10','VD14','VD16','VD20']].idxmax(axis=1).str[-2:].astype(np.float64)
family_type = family_type[['GEO.id','type']]
family_type.columns = ['Id','type']

family_type = family_type.replace('03',1)
family_type = family_type.replace('07',2)
family_type = family_type.replace('10',3)
family_type = family_type.replace('14',4)
family_type = family_type.replace('16',5)
family_type = family_type.replace('20',6)

family_type = family_type.reset_index(drop=True)

#### BEDROOMS ####
household_size = pd.read_csv('household_size.csv',skiprows=1)
household_size = household_size.drop(0)
household_size['household_size'] = household_size[['1-person household','2-person household','3-person household','4-person household','5-person household','6-person household','7-or-more person household',]].idxmax(axis=1).str[0].astype(np.float64)
household_size = household_size[['Id','household_size']]

household_size = household_size.reset_index(drop=True)

#### BEDROOMS ####
language = pd.read_csv('language.csv',header=None)
headers = language.iloc[0]
language = language[3:]
language.columns = headers

language[['VD02','VD03','VD06','VD09','VD12']] = language[['VD02','VD03','VD06','VD09','VD12']].astype(np.float64)
language = language[['GEO.id','VD02','VD03','VD06','VD09','VD12']]

language['language'] = language[['VD02','VD03','VD06','VD09','VD12']].idxmax(axis=1).str[-2:]
language = language[['GEO.id','language']]
language.columns = ['Id','language']

language = language.replace('02',np.float64(1))
language = language.replace('03',np.float64(2))
language = language.replace('06',np.float64(3))
language = language.replace('09',np.float64(4))
language = language.replace('12',np.float64(5))

language = language.reset_index(drop=True)

#### BEDROOMS ####
rent = pd.read_csv('rent.csv',skiprows=1)
rent = rent.drop(0)
rent = rent[['Id','Median gross rent']]
rent.columns = ['Id','rent']
rent = rent.replace('100-',100)
rent = rent.replace('2,000+',2000)
rent.rent = rent.rent.astype(np.float64)
rent = rent.reset_index(drop=True)


# drop missing rows
for i in DROP:
    age = age.drop(i)
    bedrooms = bedrooms.drop(i)
    family_type = family_type.drop(i)
    household_size = household_size.drop(i)
    language = language.drop(i)
    rent = rent.drop(i)


# create concatted dataframe
df = pd.concat([age, bedrooms, family_type, household_size, language, rent],axis=1)
df = df.loc[:,~df.columns.duplicated()]

def get_neighborhood(person):
    neighborhoods = {}
    for i in range(0, df.shape[0]):
        row = df.iloc[i].tolist()
        n = row.pop(0)
        neighborhoods[euclidean(row, person)] = n
    suggest = []
    keys = list(neighborhoods.keys())
    keys.sort()
    count = 0
    for key in keys:
        if neighborhoods[key] not in neighborhoods_geom.keys():
            print("Key error: "+str(neighborhoods[key]))
        else:
            count+=1
            #print("found: "+str(neighborhoods[key]))
            suggest.append(neighborhoods_geom[neighborhoods[key]])
            if count == 5: return suggest
    return suggest


#print('hello world!')
#print(len(neighborhoods_geom.keys()))
print(get_neighborhood([1,1,1,1,1,1]))
