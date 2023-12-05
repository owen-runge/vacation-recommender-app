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
    "transportation-ranking" : "Transport",
    "safety-ranking" : "Safety",
    "activity-ranking" : "Activity",
    "restaurant-ranking" : "Restaurant"
} 
#feedback survey category names
user_survey_list = ["climate-ranking", "transportation-ranking", "safety-ranking", "activity-ranking", "restaurant-ranking"]

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
        
       
def main(user_feedback_survey):  
    """
    Paramters :
    user_feedback_survey : Feedback of the cities chosen for the user based on initial user interest
    
    function : 
    Make the reinforcement Learning data update and save the updated CSV
    
    Returns: None
    CSV rfl data updated based on user feedback
    """  
    user_survey_rfl = user_feedback_survey["user_survey_rfl"]
    for index in range(len(user_survey_list)):
        update_rfl_data(user_survey_list[index], user_survey_rfl[index], user_feedback_survey)
    reinforcement_data_df.to_csv("Reinforcement_Data_Update.csv")
    

#example survey feedback
# {
#     "climate-ranking": [     
#       "Tucson, AZ",       
#       "Los Angeles, CA",      
#       "Miami, FL", 
#       "Honolulu, HI",
#       "New Orleans, LA"
#     ],
#     "transportation-ranking" : [     
#         "Tucson, AZ",       
#         "Los Angeles, CA",      
#         "Miami, FL", 
#         "Honolulu, HI",
#         "New Orleans, LA"
#     ],
#     "safety-ranking" : [
#         "Tucson, AZ",       
#         "Los Angeles, CA",      
#         "Miami, FL", 
#         "Honolulu, HI",
#         "New Orleans, LA"
#     ],
#     "activity-ranking" : [
#         "Tucson, AZ",       
#         "Los Angeles, CA",      
#         "Miami, FL", 
#         "Honolulu, HI",
#         "New Orleans, LA"
#     ],   
#     "restaurant-ranking" : [
#         "Los Angeles, CA",      
#         "Miami, FL", 
#         "Honolulu, HI",
#         "Tucson, AZ",
#         "New Orleans, LA"
#     ],
#     "user_survey_rfl": [
#         0.7723210344517383,
#         0.5,
#         0.3543806258340809,
#         0.4832442071576537,
#         0.13687061439118695
#      ]
# }

# survey_json = open('user_feedback_survey.json')
# survey_data_dict = json.load(survey_json) 
# main(survey_data_dict)    