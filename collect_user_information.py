"""
This script contains the procedure in collecting a user's information given by the TikTok API
"""

import requests
import json
import os
import pandas as pd
import time
import numpy as np
import sys


token = "<ENTER KEY HERE>"
headers = {
        'authorization': 'bearer '+token
}

#input: the path to the file
#output: return the extension of the file
def get_file_extension(file_path):
    # Split the file path into root and extension
    _, ext = os.path.splitext(file_path)
    return ext

#input: username 
#output: returns the user's information
def fetch_tiktok_data(username): 
    url='https://open.tiktokapis.com/v2/research/user/info/?fields=display_name,bio_description,avatar_url,is_verified,follower_count,following_count,likes_count,video_count'
    data = {
            'username':username
    }

    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                print(response.json())
                user_display_name = response.json()['data'].get('display_name', np.nan)
                user_follower_count= response.json()['data'].get('follower_count', np.nan)
                user_following_count = response.json()['data'].get('following_count', np.nan)
                user_is_verified=response.json()['data'].get('is_verified', np.nan)
                user_likes_count=response.json()['data'].get('likes_count', np.nan)
                user_video_count=response.json()['data'].get('video_count', np.nan)
                user_avatar_url=response.json()['data'].get('avatar_url', np.nan)
                user_bio_description=response.json()['data'].get('bio_description', np.nan)
                user_status = "public"
                print("="*100)
                return pd.Series([user_follower_count, user_following_count, user_is_verified, user_display_name, user_likes_count, user_video_count, user_avatar_url, user_bio_description,user_status],
                        index=['user_follower_count', 'user_following_count', 'user_is_verified', 'user_display_name', 'user_likes_count', 'user_video_count', 'user_avatar_url', 'user_bio_description','user_status'])
            elif response.status_code == 400 :
                print("Error:", response.status_code, response.text, "USER:",username)
                if response.text.find("is private") != -1:
                    print("Private user","="*100)
                    user_status = "private"
                    return pd.Series([None,None,None,None,None,None,None,None,user_status],
                        index=['user_follower_count', 'user_following_count', 'user_is_verified', 'user_display_name', 'user_likes_count', 'user_video_count', 'user_avatar_url', 'user_bio_description','user_status'])
                else:
                    print("="*100)
                    user_status = "deleted"
                    return pd.Series([None,None,None,None,None,None,None,None,user_status],
                        index=['user_follower_count', 'user_following_count', 'user_is_verified', 'user_display_name', 'user_likes_count', 'user_video_count', 'user_avatar_url', 'user_bio_description','user_status'])
            elif response.status_code == 401 :
                return pd.Series([None,None,None,None,None,None,None,None,None],
                        index=['user_follower_count', 'user_following_count', 'user_is_verified', 'user_display_name', 'user_likes_count', 'user_video_count', 'user_avatar_url', 'user_bio_description','user_status'])
            elif response.status_code == 429 :
                print("Error:", response.status_code, response.text, "USER:",username)
                print("="*100)
                return pd.Series([None,None,None,None,None,None,None,None,None],
                        index=['user_follower_count', 'user_following_count', 'user_is_verified', 'user_display_name', 'user_likes_count', 'user_video_count', 'user_avatar_url', 'user_bio_description','user_status'])
            else:
                print("Error:", response.status_code, response.text, "USER:",username)
                print(f"Attempt {attempt + 1} failed")
                if attempt < max_attempts - 1:
                    print("Retrying...")
                    time.sleep(50)
                else:
                    print("Max attempts reached. Moving to next URL.")
                    return pd.Series([None,None,None,None,None,None,None,None,None],
                        index=['user_follower_count', 'user_following_count', 'user_is_verified', 'user_display_name', 'user_likes_count', 'user_video_count', 'user_avatar_url', 'user_bio_description','user_status'])
        except requests.exceptions.ReadTimeout:
            # Handle timeout exception
            print("The request timed out") 
            if attempt < max_attempts - 1:
                print("Retrying...")
                time.sleep(50)
            else:
                print("Max attempts reached. Moving to next URL.")
                return pd.Series([None,None,None,None,None,None,None,None,None],
                        index=['user_follower_count', 'user_following_count', 'user_is_verified', 'user_display_name', 'user_likes_count', 'user_video_count', 'user_avatar_url', 'user_bio_description','user_status'])



# Specify the directory path 
directory = "<ENTER THE FILE PATH TO A DIRECTORY CONTAIN A FOLDER OF CSV FILES OF YOUR VIDEOS' METADATA>"


# List all files and directories in the specified path
for item in os.listdir(directory):
    # Create full path
    full_path = os.path.join(directory, item)
    #checking if the file is csv file
    if get_file_extension(full_path) == ".csv":

        fileName = item.split('.')[0]
        # Check if it's a file and not a directory
        print("Current File:",fileName)
        if os.path.isfile(full_path):
            df = pd.read_csv(full_path)
            # df = df.iloc[0:5] #grabbing the first few for testing

            # Adding empty columns
            df['user_display_name'] = None
            df['user_bio_description']=None
            df['user_avatar_url']=None
            df['user_is_verified']=None
            df['user_following_count'] = None
            df['user_follower_count']= None
            df['user_video_count']=None
            df['user_likes_count']=None
            df['user_status']=None
     
            df[['user_follower_count','user_following_count','user_is_verified','user_display_name','user_likes_count','user_video_count','user_avatar_url','user_bio_description','user_status']] = df['username'].apply(fetch_tiktok_data)
            df.to_csv(f"<PATH TO THE FOLDER WITH THE OUTPUTTED INFORMATION>/{fileName}_user_info.csv")
            print(f"************** DONE WITH {fileName} CSV FILE **************")


