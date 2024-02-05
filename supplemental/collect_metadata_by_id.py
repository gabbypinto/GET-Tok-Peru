"""
author: Gabriela Pinto
date: Feb 4, 2024

This script will query the video based on the ID, but given the json_response you can see if it is
still available through the TikTok Research API 

NOTE: the TikTok Research API doesn't allow search dates to be more than 30 days after
our data collection contains videos spanning from November 20, 2022 to March 01, 2023. If you're 
looking for an ID from our dataset, you make have to tweak the start_date and end_date

recommendation: 
start with November 20, 2022 -> December 20,2022. if that doesn't work then try December 20, 2022 -> January 20, 2023...etc
"""

import requests
import json
import pandas as pd


def grabById(row):
    """
        Retrieve the data from the TikTok API

        Parameters:
        pandas dataframe row: row from the provided file

        Returns:
        json: json response from the call
    """
    id = row['id']

    headers = {
        'authorization': 'bearer clt.BEHLay625QO8ASsCuuZKxKaFXaoXCAdI7Cdfz8azvSL2E11oRjHCRVqCz3Kz'
    }
    url = 'https://open.tiktokapis.com/v2/research/video/query/?fields=id,like_count,create_time,region_code,share_count,view_count,like_count,comment_count,music_id,hashtag_names,username,effect_ids,playlist_id,video_description,voice_to_text'
    
    data = {
            "query": {
                "and": [
                    { "operation": "EQ", "field_name": "video_id", "field_values": [id] },
                ],
            }, 
            "start_date": "20221120",
            "end_date":"20221220", 
        }
    
    response = requests.post(url, headers=headers, json=data)

    return response.json()


df = pd.read_csv("FILE PATH TO DATA HERE.csv")

df['isPublic'] = df.apply(grabById,axis=1)
df.to_csv("INSERT FILE NAME.csv",index=False)
