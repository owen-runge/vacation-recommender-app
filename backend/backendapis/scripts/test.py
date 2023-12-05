#imports
import pandas as pd
#import numpy as np 
#import seaborn as sns 
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
from additional_city_info import build_city_points
import random

#Data Structures Used to Update Values
seasons_dict = {
    'Winter' : ['Jan', 'Feb', 'Dec'],
    'Fall' : ['Sept', 'Oct', 'Nov'],
    'Spring' : ['March', 'April', 'May'],
    'Summer' : ['June', 'July', 'Aug']   
}

weather_scores = {
    'CoolDry' : 0.2,
    'CoolWet' : 0.3,
    'HotDry' : 0.9,
    'HotWet' : 1.0,
    'WarmDry' :  0.7,
    'WarmWet' : 0.8,
    'ColdDry' : 0.0,
    'ColdWet' : 0.1,
    'TemperateDry' : 0.40,
    'TemperateWet' : 0.60   
}

transport_identity = {
    'Public-Transport' : '% Public Transit-Normalized' ,
    'Car' :'% Car-Normalized' ,
    'Walking' : '% Walking-Normalized',
    'Bike' : '% Bike-Normalized'    
}

attraction_identity = {
    'spas_wellness' : 'total_spas_wellness-Normalized',
    'sights_landmarks' : 'total_sights_landmarks-Normalized',
    'nightlife' : 'total_nightlife-Normalized',
    'fun_games' :'total_fun_games-Normalized',
    'nature_parks' : 'total_nature_parks-Normalized',
    'museums' : 'total_museums-Normalized',
    'classes_workshops' : 'total_classes_workshops-Normalized',
    'boat_tours_water_sports' : 'total_boat_tours_water_sports-Normalized',
    'zoos_aquariums' : 'total_zoos_aquariums-Normalized',
    'water_amusement_parks' : 'total_water_amusement_parks-Normalized',
    'casinos_gambling' : 'total_casinos_gambling-Normalized',    
}

#Reading General CSV data
#sample survey row
cities_data_sample_row = pd.read_csv('sample_survey_row.csv', index_col = 0).squeeze('columns')
cities_data_df = pd.read_csv('suvey_normalized_data.csv')  
cities_data_df = cities_data_df.fillna(0)
cities_data_df = cities_data_df.iloc[ : , 1 :]

def user_survey_rfl(updated_sample_row):
    """
    Inputs : 
    updated_sample_row : sample row updated with values from the user survey
    
    Function : Build the ideal user survey data for reinforcment learning update in reinforcementLearning.py
    
    Outputs:
    user_survey_value_list : updated data values for the five categories used in the reinforcement learning data
     
    """
    first_row_climate = updated_sample_row.iloc[0 : 12]
    first_row_transport = updated_sample_row.iloc[38 : 42]
    first_row_safety = pd.concat([updated_sample_row.iloc[36 : 38], updated_sample_row.iloc[70 : 75]])
    first_row_activity = updated_sample_row.iloc[43 : 65]
    first_row_cuisine = pd.concat([updated_sample_row.iloc[64 : 70], updated_sample_row.iloc[75 : ]])
    climate_value = first_row_climate.sum()/first_row_climate.size
    transport_value = first_row_transport.sum()/first_row_transport.size
    safety_value = first_row_safety.sum()/ first_row_safety.size
    activity_value = first_row_activity.sum()/first_row_activity.size
    restaurant_value = first_row_cuisine.sum()/ first_row_cuisine.size
    user_survey_value_list = [climate_value, transport_value, safety_value, activity_value, restaurant_value]
    
    return user_survey_value_list

def parallel_model(updated_sample_row, survey_data_start, survey_data_end, city_data, city_data_start, city_data_end, nn_value):
    
    """
    Inputs : 
    updated_sample_row : sample row updated with values from the user survey
    survey_data_start : index of the intial feature from the sample row
    survey_data_end : index of the final feature from the sample row
    city_data : teh dataframe containing all the cities feature data
    city_data_start : index of the intial feature from the city_data
    city_data_end : index of the final feature from the city_data
    nn_value : the number of cities the model is expected to output
    
    Function : The model 
    
    Outputs:
    updated_data_df : Information of all the cities and their features output by the model
     
    """
    #updating model_data and survey_data
    survey_data_df = updated_sample_row.iloc[ survey_data_start:survey_data_end]
    model_data_df = city_data.iloc[ : , 1 : ]
    model_data_df = model_data_df.iloc[ : , city_data_start : city_data_end]
    #building model
    model=NearestNeighbors(algorithm='auto', metric='minkowski')
    model.fit(model_data_df)
    #getting choice from sample
    dist,index= model.kneighbors(survey_data_df.values.reshape(1,-1), n_neighbors= nn_value)
    first_data_point = city_data.iloc[index[0][0], : ]
    #building a new df of the chosen cities i KNN
    updated_data_df = pd.DataFrame(first_data_point)
    updated_data_df = updated_data_df.transpose()
    #adding all the cities from KNN
    index_count = 1
    while index_count < len(index[0]):
        val = index[0][index_count]
        answer_row = city_data.iloc[val , : ]
        updated_data_df  = pd.concat([ updated_data_df , answer_row.set_axis(updated_data_df.columns).to_frame().T])
        index_count += 1
    return updated_data_df

#updating the survey information using user input
def survey_update(survey_data_dict):
    """
    Inputs : 
    survey_data_dict : sample row wih all values 0.5 except cuisine which is 0
    
    Function : Build the sample survey using the user survey
    
    Outputs:
    updated_sample_survey: sample survey updated with normalized value from the user survey
     
    """
    #updating climate
    month_list = seasons_dict[survey_data_dict['time-of-year']]
    try:
        temperature_score = weather_scores[survey_data_dict['climate-choices'] + survey_data_dict['climate-humidity']]
    except:
        temperature_score = 0.5
    for col_name, col_values in cities_data_sample_row.items():
        if 'Temp' in col_name or 'Percip' in col_name or 'Humid' in col_name :
            for month in month_list:
                if month in col_name:
                    cities_data_sample_row[col_name] = temperature_score
                    break
                else:                    
                    cities_data_sample_row[col_name] = cities_data_df[col_name].quantile(temperature_score) + random.uniform(-0.05, 0.05)
    #updating health
    health_score = 0.2 * survey_data_dict['healthcare-importance']
    cities_data_sample_row['Healthcare Index-Normalized'] = cities_data_df['Healthcare Index-Normalized'].quantile(health_score) + random.uniform(-0.1, 0.1)
    cities_data_sample_row['HCI Contributors-Normalized'] = cities_data_df['HCI Contributors-Normalized'].quantile(health_score)  + random.uniform(-0.1, 0.1)

    #accidents
    accident_score =  1.2 - 0.2 * survey_data_dict['safety-importance']
    cities_data_sample_row['2019_violent_crime_ct-Normalized'] = cities_data_df['2019_violent_crime_ct-Normalized'].quantile(accident_score) + random.uniform(-0.1, 0.1)
    cities_data_sample_row['2019_property_crime_ct-Normalized'] = cities_data_df['2019_property_crime_ct-Normalized'].quantile(accident_score) + random.uniform(-0.1, 0.1)
    cities_data_sample_row['num_fatal_crashes-Normalized'] = cities_data_df['num_fatal_crashes-Normalized'].quantile(accident_score) + random.uniform(-0.1, 0.1)
    cities_data_sample_row['fatalities_per_100m_miles-Normalized'] = cities_data_df['fatalities_per_100m_miles-Normalized'].quantile(accident_score) + random.uniform(-0.1, 0.1)
    cities_data_sample_row['car_thefts_per_100k_residents-Normalized'] = cities_data_df['car_thefts_per_100k_residents-Normalized'].quantile(accident_score) + random.uniform(-0.1, 0.1)

    #hotels
    hotel_score =  0.2 * survey_data_dict['hotel-importance']
    cities_data_sample_row['total_hotels-Normalized'] = cities_data_df['total_hotels-Normalized'].quantile(hotel_score) + random.uniform(-0.1, 0.1)
    cities_data_sample_row['pct_good_hotels-Normalized'] =  cities_data_df['pct_good_hotels-Normalized'].quantile(hotel_score) + random.uniform(-0.1, 0.1)
    cities_data_sample_row['avg_rating-Normalized'] = cities_data_df['avg_rating-Normalized'].quantile(hotel_score) + random.uniform(-0.1, 0.1)
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
    transport_choices_list = survey_data_dict['transport-ranking']
    choice_subtraction = 0
    for transport in transport_choices_list:
        survey_data_dict[transport_identity[transport]] = cities_data_df[transport_identity[transport]].quantile( 1 - choice_subtraction) + random.uniform(-0.1, 0.1)
        choice_subtraction += 0.2       
    #attractions
    attraction_choices_list = survey_data_dict['activity-type-ranking']
    choice_subtraction = 0
    for attraction in attraction_choices_list:
        survey_data_dict[attraction_identity[attraction]] = cities_data_df[attraction_identity[attraction]].quantile( 1 - choice_subtraction) + random.uniform(-0.1, 0.1)
        choice_subtraction += 0.05   
        
        
    #budget
    budget_ascending_score = 0.2 * survey_data_dict['budget']
    budget_descending_score =  1.2 - 0.2 * survey_data_dict['budget']
    budget_middle_score = 1 - abs(3 - survey_data_dict['budget']) * 0.2
    cities_data_sample_row['avg_price-Normalized'] = cities_data_df['avg_price-Normalized'].quantile(budget_ascending_score ) + random.uniform(-0.1, 0.1)
    cities_data_sample_row['num_fine_dining-Normalized'] = cities_data_df['num_fine_dining-Normalized'].quantile(budget_ascending_score ) + random.uniform(-0.1, 0.1)
    cities_data_sample_row['num_michelin-Normalized'] =  cities_data_df['num_michelin-Normalized'].quantile(budget_ascending_score ) + random.uniform(-0.1, 0.1)
    cities_data_sample_row['num_cheap_eats-Normalized'] = cities_data_df['num_cheap_eats-Normalized'].quantile(budget_descending_score) + random.uniform(-0.1, 0.1)
    cities_data_sample_row['total_budget_friendly-Normalized'] = cities_data_df['total_budget_friendly-Normalized'].quantile(budget_descending_score) + random.uniform(-0.1, 0.1)
    cities_data_sample_row['num_moderately_priced-Normalized'] = cities_data_df['num_moderately_priced-Normalized'].quantile(budget_middle_score) + random.uniform(-0.1, 0.1)
    #kids
    kids_score = 0.2 * survey_data_dict['kids-attraction-importance']
    cities_data_sample_row['total_good_for_kids-Normalized'] = cities_data_df['total_good_for_kids-Normalized'].quantile(kids_score) + random.uniform(-0.1, 0.1)
    #adrenaline
    adrenaline_score = 0.2 * survey_data_dict['adrenaline-attraction-importance']
    cities_data_sample_row['total_good_for_adrenaline_seekers-Normalized'] = cities_data_df['total_good_for_adrenaline_seekers-Normalized'].quantile(adrenaline_score) + random.uniform(-0.1, 0.1)
    return cities_data_sample_row
    
    

def main(survey_data_dict):
    """
    Inputs : 
    survey_data_dict : sample row wih all values 0.5 except cuisine which is 0
    
    Function : Main function to call all the other methods to output the five optimum cities for the user
    
    Outputs:
    json_object_result : Json object returned to the Front-End with information about the five cities chosen by the model as well ideal
    data from the user survey for the reinforcementLearning updates
     
    """
    
    #month list from data structure
    month_list = seasons_dict[survey_data_dict['time-of-year']]
    #sample row update
    updated_sample_row = survey_update(survey_data_dict)
    #using the model to get closest cities to survey
    #climate
    updated_cities_df = parallel_model(updated_sample_row, 0, 12, cities_data_df, 0, 12, 25)
    #everything beetween climate and cuisine
    updated_cities_df = parallel_model(updated_sample_row, 36, 75, updated_cities_df, 36, 75, 10)
    #cuisines
    updated_cities_df = parallel_model(updated_sample_row, 75, 130, updated_cities_df, 75, 130, 5)
    city_output = updated_cities_df['City'].tolist()    
    
    #run build_city_points
    full_output = build_city_points(city_output, cities_data_sample_row, month_list, survey_data_dict)
    #reinforcement learning survey values
    user_survey_rfl_list = user_survey_rfl(updated_sample_row)
    full_output["user_survey_rfl"] = user_survey_rfl_list  
    json_object_result = json.dumps(full_output, indent=3)
    return json_object_result
    # with open(sys.argv[3], "w") as outfile:
    #     outfile.write(json_object_result)

# survey_data_dict = {
#    "climate-choices": "Hot",
#    "climate-humidity": "Dry",
#    "time-of-year": "Fall",
#    "transport-choices": [
#       "Car",
#       "Bike"
#    ],
#    "transport-ranking": [
#       "Car",
#       "Bike"
#    ],
#    "budget": 5,
#    "kids-attraction-importance": 4,
#    "adrenaline-attraction-importance": 3,
#    "activity-type-choices": [
#       "zoos_aquariums",
#       "museums",
#       "sights_landmarks",
#       "casinos_gambling",
#       "classes_workshops",
#       "nightlife"
#    ],
#    "activity-type-ranking": [
#       "casinos_gambling",
#       "museums",
#       "classes_workshops",
#       "sights_landmarks",
#       "nightlife",
#       "zoos_aquariums"
#    ],
#    "hotel-importance": 4,
#    "cuisine-choices": [
#       "American",
#       "Pizza",
#       "Latin",
#       "Southwestern",
#       "Japanese"
#    ],
#    "healthcare-importance": 5,
#    "safety-importance": 4
# }
# print(main(survey_data_dict))
#main(survey_data_dict)
#Survey Information
# survey_json = open('survey_study.json')
# survey_data_dict = json.load(survey_json)
# print(model_output(survey_data_dict))

#system 
# if sys.argv[1] == 'model_output':
#     model_output()
    
# sys.stdout.flush()