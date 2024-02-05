"""
author: Gabriela Pinto
date: Feb 4, 2024

This script calls the TikTok Research API to 
collect the metadata
"""

import requests
import json
from datetime import datetime, timedelta
import sys


def save_to_json_file(data, filename):
    """
        Save the data to a json file.

        Parameters:
        data (json): json data from the TikTok API
        filename (str): name of the file with the response

        Returns:
        None: creates a json file
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def fetch_tiktok_data(headers,start_date,end_date):
    """
        Retrieve the data from the TikTok API

        Parameters:
        data (json): json data from the TikTok API
        start_date (str): start date that will be included in our query
        end_date (str): end date that will be included in our query

        Returns:
        float: The area of the circle.
    """
    full_json_response = {}
    full_json_response['data']={}
    full_json_response['data']['videos'] = [] 

    headers = {
        'authorization': 'bearer <INSERT TOKEN>'
    }
    url = 'https://open.tiktokapis.com/v2/research/video/query/?fields=id,like_count,create_time,region_code,share_count,view_count,like_count,comment_count,music_id,hashtag_names,username,effect_ids,playlist_id,video_description,voice_to_text'
    
    data = {
            "query": {
                "and": [
                    { "operation": "IN", "field_name": "region_code", "field_values": ["PE"] },
                ],
                "or":[
                    { "operation": "EQ", "field_name": "keyword", "field_values": ["Castillo"] },
                    { "operation": "EQ", "field_name": "keyword", "field_values": ["Presidente Castillo"] },
                    { "operation": "EQ", "field_name": "keyword", "field_values": ["Pedro Castillo"] },
                    { "operation": "EQ", "field_name": "keyword", "field_values": ["Dina Boluarte"] },
                    { "operation": "EQ", "field_name": "keyword", "field_values": ["Presidente Boluarte"] },
                    { "operation": "EQ", "field_name": "keyword", "field_values": ["Boluarte"] },
                    
                    { "operation": "EQ", "field_name": "hashtag_name", "field_values": ["PedroCastillo"] },
                    { "operation": "EQ", "field_name": "hashtag_name", "field_values": ["Castillo"] },
                    { "operation": "EQ", "field_name": "hashtag_name", "field_values": ["Boluarte"] },
                    { "operation": "EQ", "field_name": "hashtag_name", "field_values": ["pedrocastillo"] },
                    { "operation": "EQ", "field_name": "hashtag_name", "field_values": ["pedrocastilloperu"] },
                    { "operation": "EQ", "field_name": "hashtag_name", "field_values": ["pedrocastilloperú"] },
                    {"operation": "EQ", "field_name": "hashtag_name", "field_values": ["golpedeestado"] },
                    {"operation": "EQ", "field_name": "hashtag_name", "field_values": ["GolpeDeEstado"] },
                    {"operation": "EQ", "field_name": "hashtag_name", "field_values": ["golpedeestadoperu"] },
                    {"operation": "EQ", "field_name": "hashtag_name", "field_values": ["crisispoliticaenperu"] },
                    {"operation": "EQ", "field_name": "hashtag_name", "field_values": ["crisispoliticaenperú"] },
                ]
            }, 
            "start_date":start_date, #the lower bound of video creation time in UTC
            "end_date":end_date, #the upper bound of video creation time in UTC
            "max_count": 100 #the number of videos in respose. This value can range between 20 and 100
        }
    
    total_count = 0
    while True:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200: #
            if response.json()["data"]["has_more"] != True:
                full_json_response['data']['videos'].extend(response.json()['data']['videos'])
                return full_json_response,total_count
            elif response.json()["data"]["has_more"] == True: 
                next_cursor = response.json()['data']['cursor']
                data['cursor'] = next_cursor
                full_json_response['data']['videos'].extend(response.json()['data']['videos'])
                total_count += len(response.json()['data']['videos'])
        elif response.status_code == 401:
            print("status code 401")
            return full_json_response,total_count
        elif response.status_code == 429: #API rate limit passed
            print("status code 429")
            return full_json_response,total_count
        elif response.status_code == 500: #internal server error
            print("status code 500")
            sys.exit() 
        else:
            print("Error:", response.status_code, response.text)
            return full_json_response,total_count
    
        

headers = {}

#start date needs to be in the format: YEARMMDD"
start_date="20221120"  

# Convert the string to a datetime object
start_date_obj = datetime.strptime(start_date, "%Y%m%d")

"""
this loop will grab data at 1 day increments (i.e. 20221120 to 20221121)
"""
while start_date != "20220301":  
    #The end date will be 1 day after the start date (i.e. start date = 20221120, end date = 20221121)
    end_date_obj = start_date_obj + timedelta(days=1)
    # Convert the new date back to string format
    end_date_str = end_date_obj.strftime("%Y%m%d")
    
    #collect the data from TikTok
    data,total = fetch_tiktok_data(headers,start_date,end_date_str)
    
    #save the data into a json file 
    if data:
        save_to_json_file(data, f'{start_date}_{end_date_str}.json')

    #increment the start date for the next iteration
    start_date_obj = datetime.strptime(start_date, "%Y%m%d")
    start_date_obj = start_date_obj + timedelta(days=1)
    start_date = start_date_obj.strftime("%Y%m%d")