#imports
import pandas as pd
import numpy as np 
import math
import json
import random

#1 ranking bring it closer to survey by 0.07
#2 ranking bring it closer to survey by 0.04
#3 ranking leave it as is 
#4 ranking move it further to survey by 0.04
#5 ranking move it further to survey by 0.07
# user_survey_value_list = [climate_value, transport_value, safety_value, activity_value, restaurant_value]

#data structures
#rfl data and survey feedback conversion
rfl_dict = {
    "climate-ranking" : "Climate",
    "transport-ranking" : "Transport",
    "safety-ranking" : "Safety",
    "activity-ranking" : "Activity",
    "cuisine-ranking" : "Restaurant"
} 
#feedback survey category names
user_survey_list = ["climate-ranking", "transport-ranking", "safety-ranking", "activity-ranking", "cuisine-ranking"]

#rfl data update increment values
survey_increment_value_list = [0.07, 0.04, 0 , -0.04, -0.07]

#data frame with the cities data
reinforcement_data_df = pd.read_csv('Reinforcement_Data_Update.csv') 

def update_rfl_data(data_category, user_category_value, user_feedback_survey):
    """  
    Paramters :
    user_feedback_survey : Feedback of the cities chosen for the user based on initial user interest
    data_category: One of Climate, Transport, Safety, Activity, Restaurant
    user_category_value: Each Category ideal user survey normalized value
    
    function : 
    Update the reinforcement learning category data based on the ideal user values as well as user feedback of the cities ranking
    
    Returns: None
    rfl dataframe updaated with data based on user feedback
    """
    cities_ranking_list = user_feedback_survey[data_category]
    dataframe_category = rfl_dict[data_category]
    for index in range(len(cities_ranking_list)):
        city = cities_ranking_list[index]
        rlf_cell_value = reinforcement_data_df.loc[reinforcement_data_df.City == city, dataframe_category].values[0]
        survey_increment_value = survey_increment_value_list[index]
        if (rlf_cell_value - user_category_value) > 0 :
            rlf_cell_value = rlf_cell_value - survey_increment_value
        else:
            rlf_cell_value = rlf_cell_value + survey_increment_value
            
        reinforcement_data_df.loc[reinforcement_data_df.City == city, dataframe_category] = rlf_cell_value
        
       
def main(user_feedback_survey, user_feedback_values):  
    """
    Paramters :
    user_feedback_survey : Feedback of the cities chosen for the user based on initial user interest
    user_feedback_values : Ideal User Survey Category Values List
    function : 
    Make the reinforcement Learning data update and save the updated CSV
    
    Returns: None
    CSV rfl data updated based on user feedback
    """  
    for index in range(len(user_survey_list)):
        update_rfl_data(user_survey_list[index], user_feedback_values[index], user_feedback_survey)
    #print(reinforcement_data_df.loc[reinforcement_data_df.City == "Oklahoma City, OK", "Climate"].values[0])
    reinforcement_data_df.to_csv("Reinforcement_Data_Update.csv")
    

#example survey feedback
#user_feedback_survey = {'climate-ranking': ['Oklahoma City, OK', 'Atlanta, GA', 'Little Rock, AR', 'Memphis, TN', 'Raleigh, NC'], 
#  'transport-ranking': ['Memphis, TN', 'Atlanta, GA', 'Oklahoma City, OK', 'Little Rock, AR', 'Raleigh, NC'],
#  'activity-ranking': ['Raleigh, NC', 'Memphis, TN', 'Atlanta, GA', 'Little Rock, AR', 'Oklahoma City, OK'],
#  'safety-ranking': ['Oklahoma City, OK', 'Atlanta, GA', 'Little Rock, AR', 'Memphis, TN', 'Raleigh, NC'], 
#  'cuisine-ranking': ['Memphis, TN', 'Atlanta, GA', 'Oklahoma City, OK', 'Little Rock, AR', 'Raleigh, NC']}

#user_feedback_value = [0.6148760226687565, 0.5, 0.20120758864903446, 0.48298553513140335, 0.09019692452251832]
# survey_json = open('user_feedback_survey.json')
# survey_data_dict = json.load(survey_json) 
#main(user_feedback_survey, user_feedback_value)    