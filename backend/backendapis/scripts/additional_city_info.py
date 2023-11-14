import pandas as pd
import numpy as np
from math import sqrt
import re
from random import randint

#all normalized data
cities_data_df = pd.read_csv('suvey_normalized_data.csv')
cities_data_df = cities_data_df.iloc[:, 1 :]

# print(cities_data_df)

# example list of 5 cities
# ex_cities = ['Baton Rouge', 'Los Angeles', 'Bismarck', 'Nashua', 'Orlando']

# data_for_ex_cities_df = cities_data_df[cities_data_df['City'].isin(ex_cities)]
# print(data_for_ex_cities_df)

# function to build the informational points for each city
def build_city_points(result_cities, cities_data_sample_row, months_list, survey_data_dict):
    """
    build_city_points

    parameters:
    - result_cities: the 5 closest cities as returned by the model
    - cities_data_sample_row: the fully built sample row for the 'city' built from the results of the survey
    - months_list: the months corresponding to the season chosen by the user
    - survey_data_dict: the raw survey results, important for formatting

    function:
    Compares the sample row to each result city in all category to determine the nearness of each metric.
    Uses this data to build a set of bullet points for each city that tell the user why each city was determined to be a good choice based on survey data

    returns:
    A dictionary where each key is the city and each value is a list of fully formatted bullet points

    """
    # get the data for all the cities returned as results form the model
    result_cities_data_df = cities_data_df[cities_data_df['City'].isin(result_cities)]

    # stats dict for mean/std dev
    all_stats = {}

    # results dict to return at the end
    results_dict = {}
    
    # calculate means, stddevs for temp and precip
    for month in months_list:
        # mean calculations for temp
        map_month_temp = result_cities_data_df['Avg.Temp.{}-Normalized'.format(month)].map(lambda x: abs(cities_data_sample_row['Avg.Temp.{}-Normalized'.format(month)] - x))
        mean_temp = map_month_temp.mean()
        # stddev calculations for temp
        stddev_temp = map_month_temp.std()

        # add values for 1 stddev from mean to all_stats as tuple
        all_stats['Avg.Temp.{}-Normalized'.format(month)] = (mean_temp-stddev_temp, mean_temp+stddev_temp)

        # mean calculations for precip
        map_month_precip = cities_data_df['Avg.Percip.{}-Normalized'.format(month)].map(lambda x: abs(cities_data_sample_row['Avg.Percip.{}-Normalized'.format(month)] - x))
        mean_precip = map_month_precip.mean()
        # stddev calculations for precip
        stddev_precip = map_month_precip.std()

        # add values for 1 stddev from mean to all_stats as tuple
        all_stats['Avg.Percip.{}-Normalized'.format(month)] = (mean_precip-stddev_precip, mean_precip+stddev_precip)

    # calculate means, stddevs for cost
    map_hotel_cost = result_cities_data_df['avg_price-Normalized'].map(lambda x: abs(cities_data_sample_row['avg_price-Normalized'] - x))
    map_att_cost = result_cities_data_df['total_budget_friendly-Normalized'].map(lambda x: abs(cities_data_sample_row['total_budget_friendly-Normalized'] - x))
    map_rst_cost = result_cities_data_df['num_cheap_eats-Normalized'].map(lambda x: abs(cities_data_sample_row['num_cheap_eats-Normalized'] - x))
    # means
    mean_hotel_cost = map_hotel_cost.mean()
    mean_att_cost = map_att_cost.mean()
    mean_rst_cost = map_rst_cost.mean()
    # stddevs
    stddev_hotel_cost = map_hotel_cost.std()
    stddev_att_cost = map_att_cost.std()
    stddev_rst_cost = map_rst_cost.std()
    # add values for 1 stddev from mean to all_stats as a tuple
    all_stats['avg_price-Normalized'] = (mean_hotel_cost-stddev_hotel_cost, mean_hotel_cost+stddev_hotel_cost)
    all_stats['total_budget_friendly-Normalized'] = (mean_att_cost-stddev_att_cost, mean_att_cost+stddev_att_cost)
    all_stats['num_cheap_eats-Normalized'] = (mean_rst_cost-stddev_rst_cost, mean_rst_cost+stddev_rst_cost)

    # calculate means, stddevs for adrenaline and kids
    map_adrenaline = result_cities_data_df['total_good_for_adrenaline_seekers-Normalized'].map(lambda x: abs(cities_data_sample_row['total_good_for_adrenaline_seekers-Normalized'] - x))
    map_kids = result_cities_data_df['total_good_for_kids-Normalized'].map(lambda x: abs(cities_data_sample_row['total_good_for_kids-Normalized'] - x))
    # means
    mean_adrenaline = map_adrenaline.mean()
    mean_kids = map_kids.mean()
    # stddevs
    stddev_adrenaline = map_adrenaline.std()
    stddev_kids = map_kids.std()
    # add values for 1 stddev from mean to all_stats as a tuple
    all_stats['total_good_for_adrenaline_seekers-Normalized'] = (mean_adrenaline-stddev_adrenaline, mean_adrenaline+stddev_adrenaline)
    all_stats['total_good_for_kids-Normalized'] = (mean_kids-stddev_kids, mean_kids+stddev_kids)

    # calculate mean, stddev for healthcare
    map_healthcare = result_cities_data_df['Healthcare Index-Normalized'].map(lambda x: abs(cities_data_sample_row['Healthcare Index-Normalized'] - x))
    # mean
    mean_healthcare = map_healthcare.mean()
    # stddev
    stddev_healthcare = map_healthcare.std()
    # add values for 1 stddev from mean to all_stats as a tuple
    all_stats['Healthcare Index-Normalized'] = (mean_healthcare-stddev_healthcare, mean_healthcare+stddev_healthcare)

    # calculate means, stddevs for safety
    map_violent_crime = result_cities_data_df['2019_violent_crime_ct-Normalized'].map(lambda x: abs(cities_data_sample_row['2019_violent_crime_ct-Normalized'] - x))
    map_property_crime = result_cities_data_df['2019_property_crime_ct-Normalized'].map(lambda x: abs(cities_data_sample_row['2019_property_crime_ct-Normalized'] - x))
    map_car_thefts = result_cities_data_df['car_thefts_per_100k_residents-Normalized'].map(lambda x: abs(cities_data_sample_row['car_thefts_per_100k_residents-Normalized'] - x))
    map_fatal_crashes = result_cities_data_df['num_fatal_crashes-Normalized'].map(lambda x: abs(cities_data_sample_row['num_fatal_crashes-Normalized'] - x))
    map_fatalities = result_cities_data_df['fatalities_per_100m_miles-Normalized'].map(lambda x: abs(cities_data_sample_row['fatalities_per_100m_miles-Normalized'] - x))
    # means
    mean_violent_crime = map_violent_crime.mean()
    mean_property_crime = map_property_crime.mean()
    mean_car_thefts = map_car_thefts.mean()
    mean_fatal_crashes = map_fatal_crashes.mean()
    mean_fatalities = map_fatalities.mean()
    # stddevs
    stddev_violent_crime = map_violent_crime.std()
    stddev_property_crime = map_property_crime.std()
    stddev_car_thefts = map_car_thefts.std()
    stddev_fatal_crashes = map_fatal_crashes.std()
    stddev_fatalities = map_fatalities.std()
    # add values for 1 stddev from mean to all_stats as a tuple
    all_stats['2019_violent_crime_ct-Normalized'] = (mean_violent_crime-stddev_violent_crime, mean_violent_crime+stddev_violent_crime)
    all_stats['2019_property_crime_ct-Normalized'] = (mean_property_crime-stddev_property_crime, mean_property_crime+stddev_property_crime)
    all_stats['car_thefts_per_100k_residents-Normalized'] = (mean_car_thefts-stddev_car_thefts, mean_car_thefts+stddev_car_thefts)
    all_stats['num_fatal_crashes-Normalized'] = (mean_fatal_crashes-stddev_fatal_crashes, mean_fatal_crashes+stddev_fatal_crashes)
    all_stats['fatalities_per_100m_miles-Normalized'] = (mean_fatalities-stddev_fatalities, mean_fatalities+stddev_fatalities)

    # calculate means, stddevs for transport
    map_walking = result_cities_data_df['% Walking-Normalized'].map(lambda x: abs(cities_data_sample_row['% Walking-Normalized'] - x))
    map_bike = result_cities_data_df['% Bike-Normalized'].map(lambda x: abs(cities_data_sample_row['% Bike-Normalized'] - x))
    map_car = result_cities_data_df['% Car-Normalized'].map(lambda x: abs(cities_data_sample_row['% Car-Normalized'] - x))
    map_public_transport = result_cities_data_df['% Public Transit-Normalized'].map(lambda x: abs(cities_data_sample_row['% Public Transit-Normalized'] - x))
    # means
    mean_walking = map_walking.mean()
    mean_bike = map_bike.mean()
    mean_car = map_car.mean()
    mean_public_transport = map_public_transport.mean()
    # stddevs
    stddev_walking = map_walking.std()
    stddev_bike = map_bike.std()
    stddev_car = map_car.std()
    stddev_public_transport = map_public_transport.std()
    # add values for 1 stddev from mean to all_stats as a tuple
    all_stats['% Walking-Normalized'] = (mean_walking-stddev_walking, mean_walking+stddev_walking)
    all_stats['% Bike-Normalized'] = (mean_bike-stddev_bike, mean_bike+stddev_bike)
    all_stats['% Car-Normalized'] = (mean_car-stddev_car, mean_car+stddev_car)
    all_stats['% Public Transit-Normalized'] = (mean_public_transport-stddev_public_transport, mean_public_transport+stddev_public_transport)

    # calculate means, stddevs for hotels
    map_rating = result_cities_data_df['avg_rating-Normalized'].map(lambda x: abs(cities_data_sample_row['avg_rating-Normalized'] - x))
    map_num_good = result_cities_data_df['num_good_hotels-Normalized'].map(lambda x: abs(cities_data_sample_row['num_good_hotels-Normalized'] - x))
    # means
    mean_rating = map_rating.mean()
    mean_num_good = map_num_good.mean()
    # stddevs
    stddev_rating = map_rating.std()
    stddev_num_good = map_num_good.std()
    # add values for 1 stddev from mean to all_stats as a tuple
    all_stats['avg_rating-Normalized'] = (mean_rating-stddev_rating, mean_rating+stddev_rating)
    all_stats['num_good_hotels-Normalized'] = (mean_num_good-stddev_num_good, mean_num_good+stddev_num_good)

    # calculate mean, stddev for activites
    map_nature_parks = result_cities_data_df['total_nature_parks-Normalized'].map(lambda x: abs(cities_data_sample_row['total_nature_parks-Normalized'] - x))
    map_fun_games = result_cities_data_df['total_fun_games-Normalized'].map(lambda x: abs(cities_data_sample_row['total_fun_games-Normalized'] - x))
    map_sights_landmarks = result_cities_data_df['total_sights_landmarks-Normalized'].map(lambda x: abs(cities_data_sample_row['total_sights_landmarks-Normalized'] - x))
    map_nightlife = result_cities_data_df['total_nightlife-Normalized'].map(lambda x: abs(cities_data_sample_row['total_nightlife-Normalized'] - x))
    map_museums = result_cities_data_df['total_museums-Normalized'].map(lambda x: abs(cities_data_sample_row['total_museums-Normalized'] - x))
    map_spas_wellness = result_cities_data_df['total_spas_wellness-Normalized'].map(lambda x: abs(cities_data_sample_row['total_spas_wellness-Normalized'] - x))
    map_classes_workshops = result_cities_data_df['total_classes_workshops-Normalized'].map(lambda x: abs(cities_data_sample_row['total_classes_workshops-Normalized'] - x))
    map_casinos_gambling = result_cities_data_df['total_casinos_gambling-Normalized'].map(lambda x: abs(cities_data_sample_row['total_casinos_gambling-Normalized'] - x))
    map_boat_tours_water_sports = result_cities_data_df['total_boat_tours_water_sports-Normalized'].map(lambda x: abs(cities_data_sample_row['total_boat_tours_water_sports-Normalized'] - x))
    map_water_amusement_parks = result_cities_data_df['total_water_amusement_parks-Normalized'].map(lambda x: abs(cities_data_sample_row['total_water_amusement_parks-Normalized'] - x))
    map_zoos_aquariums = result_cities_data_df['total_zoos_aquariums-Normalized'].map(lambda x: abs(cities_data_sample_row['total_zoos_aquariums-Normalized'] - x))
    # mean
    mean_nature_parks = map_nature_parks.mean()
    mean_fun_games = map_fun_games.mean()
    mean_sights_landmarks = map_sights_landmarks.mean()
    mean_nightlife = map_nightlife.mean()
    mean_museums = map_museums.mean()
    mean_spas_wellness = map_spas_wellness.mean()
    mean_classes_workshops = map_classes_workshops.mean()
    mean_casinos_gambling = map_casinos_gambling.mean()
    mean_boat_tours_water_sports = map_boat_tours_water_sports.mean()
    mean_water_amusement_parks = map_water_amusement_parks.mean()
    mean_zoos_aquariums = map_zoos_aquariums.mean()
    # stddev
    stddev_nature_parks = map_nature_parks.std()
    stddev_fun_games = map_fun_games.std()
    stddev_sights_landmarks = map_sights_landmarks.std()
    stddev_nightlife = map_nightlife.std()
    stddev_museums = map_museums.std()
    stddev_spas_wellness = map_spas_wellness.std()
    stddev_classes_workshops = map_classes_workshops.std()
    stddev_casinos_gambling = map_casinos_gambling.std()
    stddev_boat_tours_water_sports = map_boat_tours_water_sports.std()
    stddev_water_amusement_parks = map_water_amusement_parks.std()
    stddev_zoos_aquariums = map_zoos_aquariums.std()
    # add values for 1 stddev from mean to all_stats as a tuple
    all_stats['total_nature_parks-Normalized'] = (mean_nature_parks-stddev_nature_parks, mean_nature_parks+stddev_nature_parks)
    all_stats['total_fun_games-Normalized'] = (mean_fun_games-stddev_fun_games, mean_fun_games+stddev_fun_games)
    all_stats['total_sights_landmarks-Normalized'] = (mean_sights_landmarks-stddev_sights_landmarks, mean_sights_landmarks+stddev_sights_landmarks)
    all_stats['total_nightlife-Normalized'] = (mean_nightlife-stddev_nightlife, mean_nightlife+stddev_nightlife)
    all_stats['total_museums-Normalized'] = (mean_museums-stddev_museums, mean_museums+stddev_museums)
    all_stats['total_spas_wellness-Normalized'] = (mean_spas_wellness-stddev_spas_wellness, mean_spas_wellness+stddev_spas_wellness)
    all_stats['total_classes_workshops-Normalized'] = (mean_classes_workshops-stddev_classes_workshops, mean_classes_workshops+stddev_classes_workshops)
    all_stats['total_casinos_gambling-Normalized'] = (mean_casinos_gambling-stddev_casinos_gambling, mean_casinos_gambling+stddev_casinos_gambling)
    all_stats['total_boat_tours_water_sports-Normalized'] = (mean_boat_tours_water_sports-stddev_boat_tours_water_sports, mean_boat_tours_water_sports+stddev_boat_tours_water_sports)
    all_stats['total_water_amusement_parks-Normalized'] = (mean_water_amusement_parks-stddev_water_amusement_parks, mean_water_amusement_parks+stddev_water_amusement_parks)
    all_stats['total_zoos_aquariums-Normalized'] = (mean_zoos_aquariums-stddev_zoos_aquariums, mean_zoos_aquariums+stddev_zoos_aquariums)
    
    # cuisines data for comparison with each city
    user_chosen_cuisines = []
    for row_name, row_val in cities_data_sample_row.items():
        if 'best_cuisines' in row_name and row_val == 1.0:
            user_chosen_cuisines.append(row_name)

    # determine bullets for each category for each city
    for city in result_cities:
        # list containing all sentences for each city
        city_bullets_list = []
        # df for current city only
        curr_city_df = result_cities_data_df[result_cities_data_df['City'] == city]
        # climate
        num_close_temp_months = 0
        num_close_precip_months = 0
        if survey_data_dict['climate-choices'] == 'none':
            num_close_temp_months -= 3
        if survey_data_dict['climate-humidity'] == 'none':
            num_close_precip_months -= 3
        for month in months_list:
            curr_city_month_temp = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['Avg.Temp.{}-Normalized'.format(month)]))[0])
            if all_stats['Avg.Temp.{}-Normalized'.format(month)][0] <= abs(cities_data_sample_row['Avg.Temp.{}-Normalized'.format(month)] - curr_city_month_temp) <= all_stats['Avg.Temp.{}-Normalized'.format(month)][1]:
                num_close_temp_months += 1
            curr_city_month_precip = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['Avg.Percip.{}-Normalized'.format(month)]))[0])
            if all_stats['Avg.Percip.{}-Normalized'.format(month)][0] <= abs(cities_data_sample_row['Avg.Percip.{}-Normalized'.format(month)] - curr_city_month_precip) <= all_stats['Avg.Percip.{}-Normalized'.format(month)][1]:
                num_close_precip_months += 1
        # check if temp and precip are close and add any sentences to city_bullets_list as applicable
        if num_close_precip_months >= 2 and num_close_temp_months >= 2:
            city_bullets_list.append(climate_sentences['temp_precip_season'].format(survey_data_dict['climate-choices'],survey_data_dict['climate-humidity'],survey_data_dict['time-of-year']))
        elif num_close_precip_months >= 2:
            city_bullets_list.append(climate_sentences['precip_season'].format(survey_data_dict['climate-humidity'],survey_data_dict['time-of-year']))
        elif num_close_temp_months >= 2:
            city_bullets_list.append(climate_sentences['temp_season'].format(survey_data_dict['climate-choices'],survey_data_dict['time-of-year']))

        # cost
        has_cheap_hotels = False
        has_cheap_atts = False
        has_cheap_rsts = False
        curr_city_hotel_price = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['avg_price-Normalized']))[0])
        if (all_stats['avg_price-Normalized'][0] <= abs(cities_data_sample_row['avg_price-Normalized'] - curr_city_hotel_price) <= all_stats['avg_price-Normalized'][1]) and survey_data_dict['budget'] < 3:
            has_cheap_hotels = True
        curr_city_att_price = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['total_budget_friendly-Normalized']))[0])
        if (all_stats['total_budget_friendly-Normalized'][0] <= abs(cities_data_sample_row['total_budget_friendly-Normalized'] - curr_city_att_price) <= all_stats['total_budget_friendly-Normalized'][1]) and survey_data_dict['budget'] < 3:
            has_cheap_atts = True
        curr_city_rst_price = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['num_cheap_eats-Normalized']))[0])
        if (all_stats['num_cheap_eats-Normalized'][0] <= abs(cities_data_sample_row['num_cheap_eats-Normalized'] - curr_city_rst_price) <= all_stats['num_cheap_eats-Normalized'][1]) and survey_data_dict['budget'] < 3:
            has_cheap_rsts = True
        # add any sentences to city_bullets_list as applicable
        if has_cheap_hotels and has_cheap_atts and has_cheap_rsts:
            city_bullets_list.append(cost_sentences[randint(1000,3999)//1000].format('hotels, attractions, and restaurants'))
        elif has_cheap_hotels and has_cheap_atts:
            city_bullets_list.append(cost_sentences[randint(1000,3999)//1000].format('hotels and attractions'))
        elif has_cheap_hotels and has_cheap_rsts:
            city_bullets_list.append(cost_sentences[randint(1000,3999)//1000].format('hotels and restaurants'))
        elif has_cheap_atts and has_cheap_rsts:
            city_bullets_list.append(cost_sentences[randint(1000,3999)//1000].format('attractions and restaurants'))
    
        # adrenaline
        curr_city_adrenaline = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['total_good_for_adrenaline_seekers-Normalized']))[0])
        if (all_stats['total_good_for_adrenaline_seekers-Normalized'][0] <= abs(cities_data_sample_row['total_good_for_adrenaline_seekers-Normalized'] - curr_city_adrenaline) <= all_stats['total_good_for_adrenaline_seekers-Normalized'][1]) and survey_data_dict['adrenaline-attraction-importance'] > 3:
            city_bullets_list.append(adrenaline_sentences[randint(1000,2999)//1000])

        # kids
        curr_city_kids = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['total_good_for_kids-Normalized']))[0])
        if (all_stats['total_good_for_kids-Normalized'][0] <= abs(cities_data_sample_row['total_good_for_kids-Normalized'] - curr_city_kids) <= all_stats['total_good_for_kids-Normalized'][1]) and survey_data_dict['kids-attraction-importance'] > 3:
            city_bullets_list.append(kids_sentences[randint(1000,4999)//1000])

        # healthcare
        curr_city_healthcare = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['Healthcare Index-Normalized']))[0])
        if (all_stats['Healthcare Index-Normalized'][0] <= abs(cities_data_sample_row['Healthcare Index-Normalized'] - curr_city_healthcare) <= all_stats['Healthcare Index-Normalized'][1]) and survey_data_dict['healthcare-importance'] > 3:
            city_bullets_list.append(healthcare_sentences[randint(1000,2999)//1000])

        # safety
        curr_city_violent_crime = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['2019_violent_crime_ct-Normalized']))[0])
        curr_city_property_crime = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['2019_property_crime_ct-Normalized']))[0])
        curr_city_car_thefts = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['car_thefts_per_100k_residents-Normalized']))[0])
        curr_city_fatal_crashes = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['num_fatal_crashes-Normalized']))[0])
        curr_city_fatalities = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['fatalities_per_100m_miles-Normalized']))[0])
        crime_stats_match_ct = 0        # count number of crime stats that match
        safety_stats_match_ct = 0       # count number of safety stats that match
        if (all_stats['2019_violent_crime_ct-Normalized'][0] <= abs(cities_data_sample_row['2019_violent_crime_ct-Normalized'] - curr_city_violent_crime) <= all_stats['2019_violent_crime_ct-Normalized'][1]) and survey_data_dict['safety-importance'] > 3:
            crime_stats_match_ct += 1
        if (all_stats['2019_property_crime_ct-Normalized'][0] <= abs(cities_data_sample_row['2019_property_crime_ct-Normalized'] - curr_city_property_crime) <= all_stats['2019_property_crime_ct-Normalized'][1]) and survey_data_dict['safety-importance'] > 3:
            crime_stats_match_ct += 1
        if (all_stats['car_thefts_per_100k_residents-Normalized'][0] <= abs(cities_data_sample_row['car_thefts_per_100k_residents-Normalized'] - curr_city_car_thefts) <= all_stats['car_thefts_per_100k_residents-Normalized'][1]) and survey_data_dict['safety-importance'] > 3:
            crime_stats_match_ct += 1
        if (all_stats['num_fatal_crashes-Normalized'][0] <= abs(cities_data_sample_row['num_fatal_crashes-Normalized'] - curr_city_fatal_crashes) <= all_stats['num_fatal_crashes-Normalized'][1]) and survey_data_dict['safety-importance'] > 3:
            safety_stats_match_ct += 1
        if (all_stats['fatalities_per_100m_miles-Normalized'][0] <= abs(cities_data_sample_row['fatalities_per_100m_miles-Normalized'] - curr_city_fatalities) <= all_stats['fatalities_per_100m_miles-Normalized'][1]) and survey_data_dict['safety-importance'] > 3:
            safety_stats_match_ct += 1
        # check counts to determine which sentence, if any, should be added
        if crime_stats_match_ct >= 2 and safety_stats_match_ct >= 1:
            city_bullets_list.append(safety_sentences[randint(1000,3999)//1000])

        # transport
        curr_city_walking = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['% Walking-Normalized']))[0])
        curr_city_car = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['% Car-Normalized']))[0])
        curr_city_bike = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['% Bike-Normalized']))[0])
        curr_city_public_transport = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['% Public Transit-Normalized']))[0])
        is_good_walking = False
        is_good_car = False
        is_good_bike = False
        is_good_public_transport = False
        if (all_stats['% Walking-Normalized'][0] <= abs(cities_data_sample_row['% Walking-Normalized'] - curr_city_walking) <= all_stats['% Walking-Normalized'][1]) and ('Walking' in survey_data_dict['transport-choices']):
            is_good_walking = True
        if (all_stats['% Car-Normalized'][0] <= abs(cities_data_sample_row['% Car-Normalized'] - curr_city_car) <= all_stats['% Car-Normalized'][1]) and ('Car' in survey_data_dict['transport-choices']):
            is_good_car = True
        if (all_stats['% Bike-Normalized'][0] <= abs(cities_data_sample_row['% Bike-Normalized'] - curr_city_bike) <= all_stats['% Bike-Normalized'][1]) and ('Bike' in survey_data_dict['transport-choices']):
            is_good_bike = True
        if (all_stats['% Public Transit-Normalized'][0] <= abs(cities_data_sample_row['% Public Transit-Normalized'] - curr_city_public_transport) <= all_stats['% Public Transit-Normalized'][1]) and ('Public-Transport' in survey_data_dict['transport-choices']):
            is_good_public_transport = True
        # check bools to determine which sentence, if any, should be used
        if is_good_walking and not (is_good_car or is_good_bike or is_good_public_transport):           # if city is only good for walking
            city_bullets_list.append(transport_sentences['walk'])
        elif is_good_car and not (is_good_walking or is_good_bike or is_good_public_transport):         # if city is only good for cars
            city_bullets_list.append(transport_sentences['car'])
        elif is_good_bike and not (is_good_walking or is_good_car or is_good_public_transport):         # if city is only good for bikes
            city_bullets_list.append(transport_sentences['bike'])
        elif is_good_public_transport and not (is_good_walking or is_good_car or is_good_bike):         # if city is only good for public transport
            rand_ind = randint(1000,2999)//1000
            if rand_ind == 1:
                city_bullets_list.append(transport_sentences['public_transport'])
            else:
                city_bullets_list.append(transport_sentences['public_transport2'])
        elif (is_good_walking and is_good_car and is_good_bike) and not is_good_public_transport:       # if city is good for walking, cars, and bikes but not public transport
            city_bullets_list.append(transport_sentences['car_bike_walk'].format('walkable, bikeable, and driveable'))
        elif (is_good_walking and is_good_car) and not (is_good_bike and is_good_public_transport):     # if city is good for walking and cars but not biking and public transport
            city_bullets_list.append(transport_sentences['car_bike_walk'].format('walkable and driveable'))
        elif (is_good_walking and is_good_bike) and not (is_good_car and is_good_public_transport):     # if city is good for walking and biking but not cars and public transport
            city_bullets_list.append(transport_sentences['car_bike_walk'].format('walkable and bikeable'))
        elif (is_good_car and is_good_bike) and not (is_good_walking and is_good_public_transport):     # if city is good for cars and biking but not walking and public transport
            city_bullets_list.append(transport_sentences['car_bike_walk'].format('driveable and bikeable'))
        elif is_good_public_transport and is_good_bike and is_good_car and is_good_walking:             # if city is good for all 4 types of transport
            city_bullets_list.append(transport_sentences['any'].format('car, pedestrian, bike, and public transit'))
        elif (is_good_public_transport and is_good_bike and is_good_car) and not is_good_walking:       # if city is good for public transport, biking, and cars but not walking
            city_bullets_list.append(transport_sentences['any'].format('car, bike, and public transit'))
        elif (is_good_public_transport and is_good_bike and is_good_walking) and not is_good_car:       # if city is good for public transport, biking, and walking but not cars
            city_bullets_list.append(transport_sentences['any'].format('bike, pedestrian, and public transit'))
        elif (is_good_public_transport and is_good_car and is_good_walking) and not is_good_bike:       # if city is good for public transport, cars, and walking but not biking
            city_bullets_list.append(transport_sentences['any'].format('public transit, car, and pedestrian'))
        elif (is_good_public_transport and is_good_bike) and not (is_good_car and is_good_walking):     # if city is good for public transport and biking but not cars and walking
            city_bullets_list.append(transport_sentences['any'].format('biking and public transit'))
        elif (is_good_public_transport and is_good_car) and not (is_good_bike and is_good_walking):     # if city is good for public transport and cars but not walking and biking
            city_bullets_list.append(transport_sentences['any'].format('public transit and car'))
        elif (is_good_public_transport and is_good_walking) and not (is_good_car and is_good_bike):     # if city is good for public transport and walking but not cars and biking
            city_bullets_list.append(transport_sentences['any'].format('pedestrian and public transit'))

        # hotels
        curr_city_hotel_rating = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['avg_rating-Normalized']))[0])
        curr_city_num_good_hotels = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['num_good_hotels-Normalized']))[0])
        has_good_hotel_rating = False
        has_many_good_hotels = False
        if (all_stats['avg_rating-Normalized'][0] <= abs(cities_data_sample_row['avg_rating-Normalized'] - curr_city_hotel_rating) <= all_stats['avg_rating-Normalized'][1]) and survey_data_dict['hotel-importance'] > 3:
            has_good_hotel_rating = True
        if (all_stats['num_good_hotels-Normalized'][0] <= abs(cities_data_sample_row['num_good_hotels-Normalized'] - curr_city_num_good_hotels) <= all_stats['num_good_hotels-Normalized'][1]) and survey_data_dict['hotel-importance'] > 3:
            has_many_good_hotels = True
        # check bools to add a sentence if necessary
        if has_good_hotel_rating and has_many_good_hotels:
            city_bullets_list.append(hotel_sentences[randint(1000,3999)//1000])

        # activities
        top_five_activites = survey_data_dict['activity-type-ranking'][:3]
        curr_city_nature_parks = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['total_nature_parks-Normalized']))[0])
        curr_city_fun_games = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['total_fun_games-Normalized']))[0])
        curr_city_sights_landmarks = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['total_sights_landmarks-Normalized']))[0])
        curr_city_nightlife = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['total_nightlife-Normalized']))[0])
        curr_city_museums = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['total_museums-Normalized']))[0])
        curr_city_spas_wellness = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['total_spas_wellness-Normalized']))[0])
        curr_city_classes_workshops = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['total_classes_workshops-Normalized']))[0])
        curr_city_casinos_gambling = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['total_casinos_gambling-Normalized']))[0])
        curr_city_boat_tours_water_sports = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['total_boat_tours_water_sports-Normalized']))[0])
        curr_city_water_amusement_parks = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['total_water_amusement_parks-Normalized']))[0])
        curr_city_zoos_aquariums = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['total_zoos_aquariums-Normalized']))[0])
        has_nature_parks = False
        has_fun_games = False
        has_sights_landmarks = False
        has_nightlife = False
        has_museums = False
        has_spas_wellness = False
        has_classes_workshops = False
        has_casinos_gambling = False
        has_boat_tours_water_sports = False
        has_water_amusement_parks = False
        has_zoos_aquariums = False
        if (all_stats['total_nature_parks-Normalized'][0] <= abs(cities_data_sample_row['total_nature_parks-Normalized'] - curr_city_nature_parks) <= all_stats['total_nature_parks-Normalized'][1]) and ('nature_parks' in top_five_activites):
            has_nature_parks = True
        if (all_stats['total_fun_games-Normalized'][0] <= abs(cities_data_sample_row['total_fun_games-Normalized'] - curr_city_fun_games) <= all_stats['total_fun_games-Normalized'][1]) and ('fun_games' in top_five_activites):
            has_fun_games = True
        if (all_stats['total_sights_landmarks-Normalized'][0] <= abs(cities_data_sample_row['total_sights_landmarks-Normalized'] - curr_city_sights_landmarks) <= all_stats['total_sights_landmarks-Normalized'][1]) and ('sights_landmarks' in top_five_activites):
            has_sights_landmarks = True
        if (all_stats['total_nightlife-Normalized'][0] <= abs(cities_data_sample_row['total_nightlife-Normalized'] - curr_city_nightlife) <= all_stats['total_nightlife-Normalized'][1]) and ('nightlife' in top_five_activites):
            has_nightlife = True
        if (all_stats['total_museums-Normalized'][0] <= abs(cities_data_sample_row['total_museums-Normalized'] - curr_city_museums) <= all_stats['total_museums-Normalized'][1]) and ('museums' in top_five_activites):
            has_museums = True
        if (all_stats['total_spas_wellness-Normalized'][0] <= abs(cities_data_sample_row['total_spas_wellness-Normalized'] - curr_city_spas_wellness) <= all_stats['total_spas_wellness-Normalized'][1]) and ('spas_wellness' in top_five_activites):
            has_spas_wellness = True
        if (all_stats['total_classes_workshops-Normalized'][0] <= abs(cities_data_sample_row['total_classes_workshops-Normalized'] - curr_city_classes_workshops) <= all_stats['total_classes_workshops-Normalized'][1]) and ('classes_workshops' in top_five_activites):
            has_classes_workshops = True
        if (all_stats['total_casinos_gambling-Normalized'][0] <= abs(cities_data_sample_row['total_casinos_gambling-Normalized'] - curr_city_casinos_gambling) <= all_stats['total_casinos_gambling-Normalized'][1]) and ('casinos_gambling' in top_five_activites):
            has_casinos_gambling = True
        if (all_stats['total_boat_tours_water_sports-Normalized'][0] <= abs(cities_data_sample_row['total_boat_tours_water_sports-Normalized'] - curr_city_boat_tours_water_sports) <= all_stats['total_boat_tours_water_sports-Normalized'][1]) and ('boat_tours_water_sports' in top_five_activites):
            has_boat_tours_water_sports = True
        if (all_stats['total_water_amusement_parks-Normalized'][0] <= abs(cities_data_sample_row['total_water_amusement_parks-Normalized'] - curr_city_water_amusement_parks) <= all_stats['total_water_amusement_parks-Normalized'][1]) and ('water_amusement_parks' in top_five_activites):
            has_water_amusement_parks = True
        if (all_stats['total_zoos_aquariums-Normalized'][0] <= abs(cities_data_sample_row['total_zoos_aquariums-Normalized'] - curr_city_zoos_aquariums) <= all_stats['total_zoos_aquariums-Normalized'][1]) and ('zoos_aquariums' in top_five_activites):
            has_zoos_aquariums = True
        str_nature_parks = attraction_sentences['nature'] if has_nature_parks else ''
        str_fun_games = attraction_sentences['fun'] if has_fun_games else ''
        str_sights_landmarks = attraction_sentences['sights'] if has_sights_landmarks else ''
        str_nightlife = attraction_sentences['nighlife'] if has_nightlife else ''
        str_museums = attraction_sentences['museums'] if has_museums else ''
        str_spas_wellness = attraction_sentences['spas'] if has_spas_wellness else ''
        str_classes_workshops = attraction_sentences['classes'] if has_classes_workshops else ''
        str_casinos_gambling = attraction_sentences['casinos'] if has_casinos_gambling else ''
        str_boat_tours_water_sports = attraction_sentences['water'] if has_boat_tours_water_sports else ''
        str_water_amusement_parks = attraction_sentences['amusement_parks'] if has_water_amusement_parks else ''
        str_zoos_aquariums = attraction_sentences['zoos'] if has_zoos_aquariums else ''
        full_str = str_nature_parks + str_fun_games + str_sights_landmarks + str_nightlife + str_museums + str_spas_wellness + str_classes_workshops + str_casinos_gambling + str_boat_tours_water_sports + str_water_amusement_parks + str_zoos_aquariums
        full_str = full_str[:-2].capitalize()
        if len(full_str) >= 1:
            city_bullets_list.append(full_str)

        # cuisines
        curr_city_matching_cuisines = ""
        for cuisine in user_chosen_cuisines:
            if float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df[cuisine]))[0]) == 1.0:
                curr_city_matching_cuisines += cuisine.replace('best_cuisines-','').replace('-Normalized','') + ", "
        # check curr_city_matching_cuisines for values and add sentence to city_bullets_list if applicable
        curr_city_num_michelin = float(re.findall(r'(?<=[ -])\d+(?:\.\d+)?', str(curr_city_df['num_michelin-Normalized']))[0])
        if len(curr_city_matching_cuisines) >= 1 and curr_city_num_michelin > 0.5 and survey_data_dict['budget'] == 5:      # for cities with michelin establishments and if the user specified they have a high budget
            city_bullets_list.append(cuisine_sentences[6].format(curr_city_matching_cuisines[:-2]))
        elif len(curr_city_matching_cuisines) >= 1:                                                                         # for cuisines, no michelin
            city_bullets_list.append(cuisine_sentences[randint(1000,5999)//1000].format(curr_city_matching_cuisines[:-2]))

        results_dict[city] = city_bullets_list

    return results_dict
        


# climate sentences to be formatted based on matching data
climate_sentences = {
    'temp_season': 'Weather is {} during {}',
    'temp_precip_season': 'Weather is {} and {} during {}',
    'precip_season': 'Weather is {} during {}'
}

# cost sentences
# will need to be formatted with completed list depending on nearness of attractions, hotels, and restaurants
cost_sentences = {
    1: 'Plenty of inexpensive {}',
    2: 'Low-cost {}',
    3: 'Many reasonably priced {}'
}

# adrenaline seeker sentences
# no need for formatting
adrenaline_sentences = {
    1: 'Lots of thrilling activities for adrenaline seekers',
    2: 'Many attractions available for adrenaline seekers'
}

# good for kids sentences
# no need for formatting
kids_sentences = {
    1: 'Great for kids',
    2: 'Welcoming to kids',
    3: 'Fantastic place to bring kids',
    4: 'Plenty to do for kids'
}

# healthcare sentences
# no need for formatting
healthcare_sentences = {
    1: 'Abundance of responsive healthcare services',
    2: 'Healthcare services are very accessible'
}

# safety sentences
# no need for formatting
safety_sentences = {
    1: 'Very safe city',
    2: 'Low crime rate',
    3: 'Safe place to travel'
}

# transport points
transport_sentences = {
    'any': 'Excellent {} infrastructure',
    'public_transport': 'High availability of public transport',
    'car_bike_walk': 'Highly {} city',
    'car': 'Easy to travel around in a car',
    'bike': 'Easy to travel around by bike',
    'walk': 'Easy to travel around on foot',
    'public_transport2': 'Easy to travel around using public transport'
}

# hotel sentences
# no need for formatting
hotel_sentences = {
    1: 'Many high quality hotels',
    2: 'Abundance of highly-rated hotels',
    3: 'Tons of great hotels to choose from'
}

# attraction sentences
# one for each type of attraction, can be stringed together if multiple fit
attraction_sentences = {
    'spas': 'many spas to choose from, ',
    'sights': 'plenty of sights to see, ',
    'nighlife': 'great nightlife scene, ',
    'fun': 'lots of fun activities, ',
    'nature': 'lots of nature to enjoy, ',
    'museums': 'many museums available to visit, ',
    'classes': 'tons of workshops available to attend, ',
    'water': 'lots of activities out on the water, ',
    'zoos': 'lots of zoos and aquariums to visit, ',
    'amusement_parks': 'enjoyable amusement parks in the area, ',
    'casinos': 'plenty of casinos, '
}

# cuisine sentences
# includes michelin restaurant consideration for #6
cuisine_sentences = {
    1: 'Full of {} restaurants to try',
    2: 'Plenty of {} restaurants',
    3: 'Lots of {} restaurants',
    4: 'Great amount of {} cuisine',
    5: 'Many highly-rated restaurants serving {} cuisine',
    6: 'Many {} restaurants as well as Michelin-rated establishments'
}