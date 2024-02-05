"""
author: Gabriela Pinto 
date: Feb 4, 2024

This script will check if the video is still publicly available
"""


import pandas as pd 
import pyktok as pyk
import time
import requests
from requests.exceptions import ReadTimeout, ConnectTimeout

def isPublic(row):
    """
        Check if the video is still public on TikTok

        Parameters:
        pandas dataframe row: the row of the pandas dataframe
        
        Returns:
        boolean: True if the video is public, False if it's private
    """

    username = row['username']
    id = row['id']
    max_attempts = 10
    
    for attempt in range(max_attempts):
        try:
            tt_json = pyk.alt_get_tiktok_json(f"https://www.tiktok.com/@{username}/video/{id}?is_copy_url=1&is_from_webapp=v1")
            obj = tt_json["__DEFAULT_SCOPE__"]['webapp.video-detail']['itemInfo']['itemStruct']['privateItem']
            if obj == True: #video is private / privateItem == True
                return False
            else: #video is public / privateItem == False
                return True 
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if isinstance(e, ReadTimeout):
                if attempt < max_attempts - 1:
                    print("Retrying...")
                    time.sleep(100)  # Consider adjusting sleep time as needed
                else:
                    print("Max attempts reached. Moving to next URL.")
                    print("="*100)
                    return False  # Indicate failure to retrieve data
            elif "webapp.video-detail" in str(e) or "itemInfo" in str(e):
                return False
            else:
                print("Unhandled error, moving to next URL.")
                print(f"Attempt {attempt + 1} failed with error: {e}")
                if attempt < max_attempts - 1:
                    print("Retrying...")
                    print("="*100)
                    time.sleep(100)  # Consider adjusting sleep time as needed
                else:
                    print("Max attempts reached. Moving to next URL.")
                    print("="*100)
                    return False 
                

pyk.specify_browser('chrome')

#read your file. change FILENAME to the name of your file
df = pd.read_csv(f"FILENAME.csv")

#create a new attribute 'isPublic', checks if the video is still publicly available
df['isPublic'] = df.apply(isPublic,axis=1)
df.to_csv("FINAL.csv",index=False)
