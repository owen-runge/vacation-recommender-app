#imports
import pandas as pd
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from numpy import isnan
from pandas import read_csv
from sklearn.impute import KNNImputer
from scipy.cluster.hierarchy import linkage,dendrogram,cut_tree
from sklearn.decomposition import KernelPCA
import sys
import re
import math
import json

#Data Structures Used to Update Values
seasons_dict = {
    'Winter' : ['Jan', 'Feb', 'Dec'],
    'Fall' : ['Sept', 'Oct', 'Nov'],
    'Spring' : ['March', 'April', 'May'],
    'Summer' : ['June', 'July', 'Aug']   
}

weather_scores = {
    'Cool' : 0.35,
    'Hot' : 0.8,
    'Warm' :  0.65,
    'Cold' : 0.2,
    'Temperate' : 0.5,
    'none' : 0.5
    
}


def model_output(survey_data_dict):
    #getting the survey input
    #survey_json = open(sys.argv[2])
    # survey_data_dict = json.load(sys.argv[2])
    # survey_data_dict = json.load(survey_data)
    #sample survey row
    # cities_data_sample_row = pd.read_csv('sample_survey_row.csv', index_col = 0, squeeze = True)
    cities_data_sample_row = pd.read_csv('sample_survey_row.csv', index_col = 0).squeeze('columns')
    #all normalized data
    cities_data_df = pd.read_csv('suvey_normalized_data.csv')
    cities_data_df = cities_data_df.iloc[:, 1 :]
    #Survey Information
    #Specific Survey Topics
    month_list = seasons_dict[survey_data_dict['time-of-year']]
    temperature_score = weather_scores[survey_data_dict['climate-choices']]
    for col_name, col_values in cities_data_sample_row.items():
        if 'Temp' in col_name:
            for month in month_list:
                if month in col_name:
                    cities_data_sample_row[col_name] = temperature_score
        else:
            for month in month_list:
                if month in col_name:
                        if survey_data_dict['climate-humidity'] == 'Dry':
                            cities_data_sample_row[col_name] = 0.25
                        if survey_data_dict['climate-humidity'] == 'Wet':
                            cities_data_sample_row[col_name] = 0.75

    #updating health
    health_score = 0.2 * survey_data_dict['healthcare-importance']
    cities_data_sample_row['Healthcare Index-Normalized'] = health_score
    cities_data_sample_row['HCI Contributors-Normalized'] = health_score

    #accidents
    accident_score =  1.2 - 0.2 * survey_data_dict['safety-importance']
    cities_data_sample_row['2019_violent_crime_ct-Normalized'] = accident_score
    cities_data_sample_row['2019_property_crime_ct-Normalized'] = accident_score
    cities_data_sample_row['num_fatal_crashes-Normalized'] = accident_score
    cities_data_sample_row['fatalities_per_100m_miles-Normalized'] = accident_score
    cities_data_sample_row['car_thefts_per_100k_residents-Normalized'] = accident_score

    #hotels
    hotel_score =  0.2 * survey_data_dict['hotel-importance']
    cities_data_sample_row['total_hotels-Normalized'] = hotel_score
    cities_data_sample_row['pct_good_hotels-Normalized'] = hotel_score
    cities_data_sample_row['avg_rating-Normalized'] =-hotel_score 
    #cuisines
    cuisine_list = survey_data_dict['cuisine-choices']
    for cuisine in cuisine_list :
        try:
            row_col_name = 'best_cuisines-' + cuisine + '-Normalized'
            if row_col_name in cities_data_sample_row :
                cities_data_sample_row[row_col_name] = 1 
        except:
            pass
            
    #Transport
    #attractions
    #budget
    budget_ascending_score = 0.2 * survey_data_dict['budget']
    budget_descending_score =  1.2 - 0.2 * survey_data_dict['budget']
    budget_middle_score = 1 - abs(3 - survey_data_dict['budget']) * 0.2
    cities_data_sample_row['avg_price-Normalized'] = budget_ascending_score
    cities_data_sample_row['num_fine_dining-Normalized'] =   budget_ascending_score
    cities_data_sample_row['num_michelin-Normalized'] =   budget_ascending_score
    cities_data_sample_row['num_cheap_eats-Normalized'] =   budget_descending_score
    cities_data_sample_row['total_budget_friendly-Normalized'] =   budget_descending_score
    cities_data_sample_row['num_moderately_priced-Normalized'] =   budget_middle_score
    #kids
    kids_score = 0.2 * survey_data_dict['kids-attraction-importance']
    cities_data_sample_row['total_good_for_kids-Normalized'] = kids_score
    #adrenaline
    adrenaline_score = 0.2 * survey_data_dict['adrenaline-attraction-importance']
    cities_data_sample_row['total_good_for_adrenaline_seekers-Normalized'] = adrenaline_score

    #model
    #fillna full data
    cities_data_df = cities_data_df.fillna(0)
    cities_data_model_df = cities_data_df.iloc[ : , 1 : ]
    #training 
    model=NearestNeighbors(algorithm='auto', metric='cosine')
    model.fit(cities_data_model_df)
    #getting choice from sample
    dist,index= model.kneighbors(cities_data_sample_row.values.reshape(1,-1), n_neighbors=5)    
    #final output
    #getting rid of index
    #cities_data_df = cities_data_df.to_string(index=False)
    city_output = []    
    for val in index[0]:
        #answer_row = cities_data_df.iloc[val , 0 ]
        #print(cities_data_df.iloc[val , 0 ])
        answer_city = str(cities_data_df['City'].values[val])
        city_output.append(str(answer_city))
    
    #subprocess return stuff
    json_object_result = json.dumps(city_output, indent=3)
    return json_object_result
    # with open(sys.argv[3], "w") as outfile:
    #     outfile.write(json_object_result)

# survey_data_dict = {
#    "climate-choices": "none",
#    "climate-humidity": "Dry",
#    "time-of-year": "Fall",
#    "transport-choices": [
#       "Public-Transport",
#       "Bike"
#    ],
#    "transport-ranking": [
#       "Public-Transport",
#       "Bike"
#    ],
#    "budget": 1,
#    "kids-attraction-importance": 4,
#    "adrenaline-attraction-importance": 3,
#    "activity-type-choices": [
#       "Zoos-Aquariums",
#       "Museums",
#       "Sights-Landmarks",
#       "Casinos-Gambling"
#    ],
#    "activity-type-ranking": [
#       "Casinos-Gambling",
#       "Museums",
#       "Sights-Landmarks",
#       "Zoos-Aquariums"
#    ],
#    "hotel-importance": 2,
#    "cuisine-choices": [
#       "Armenian",
#       "Central-Italian",
#       "Central-American",
#       "Central-Asian",
#       "Central-European"
#    ],
#    "healthcare-importance": 5,
#    "safety-importance": 5
# }

# print(model_output(survey_data_dict))
#Survey Information
# survey_json = open('survey_study.json')
# survey_data_dict = json.load(survey_json)
# print(model_output(survey_data_dict))

#system 
# if sys.argv[1] == 'model_output':
#     model_output()
    
# sys.stdout.flush()