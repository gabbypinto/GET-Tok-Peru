import pyktok as pyk
import os
import pandas as pd
import requests
import time 

def create_url(row):
    """
        Parameters:
        Pandas row: row from your dataframe, which contains the username and video id (id attribute)
        
        Returns:
        str: formatted url required for pyktok
    """
    username = row['username']
    videoid = row['id']
    return f"https://www.tiktok.com/@{username}/video/{videoid}"


def format_url(url):
    """
        Parameters:
        str: url to the tiktok video
        Returns:
        str: formatted url required for pyktok
    """
    return url+'?is_copy_url=1&is_from_webapp=v1'

def save_video(url):
    """
        Downloads the video given the url

        Parameters:
        str: string that is in the url formatted require for pyk: 

        Returns:
        None: The video will download in the current directory
    """
    pyk.save_tiktok(url,save_video=True,browser_name="chrome")

def download(url):
    """
        Retrieve the data from the TikTok API

        Parameters:
        str: url, the construct url outputted in the create_url function
        
        Returns:
        None
    """
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            time.sleep(10)
            formatted_url = format_url(url)
            save_video(formatted_url) #download videos here
            #if the videos downloaded..this doesn't guaranteed that it downloaded properly 
            #(i.e. it maybe download an empty mp4 file)
            return #it does exist
        except requests.exceptions.MissingSchema: 
            #invalid URL error            
            return #it doesn't exist
        except Exception as e:
            #if the webpage didn't load properly then we will call pyktok again
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt < max_attempts - 1:
                print("Retrying...")
                time.sleep(100)
            else:
                print("Max attempts reached. Moving to next URL.")
                return  # or any other indicator of failure


start_time = time.perf_counter()
pyk.specify_browser('chrome') 

full_path = "<PATH TO YOUR CSV FILE>"
try:
    df = pd.read_csv(full_path)
    file_name_with_extension = full_path.split('/')[-1]
    file_name_parts = file_name_with_extension.split('.')
    item = '.'.join(file_name_parts[:-1])  #this is the name of the input file (withou the exntension)
    #the new directory's name is based on the name of the csv file
    new_directory = item
    #where we will store our videos
    os.makedirs(new_directory, exist_ok=True)
    #change into the new directory so the videos are saved there
    os.chdir(new_directory)
    print(f"Current Working Directory: {os.getcwd()}")

    #create the url to the video
    df['tiktokurl'] = df.apply(create_url,axis=1)

    #download the videos
    df['tiktokurl'].apply(download)
              
    os.chdir('..')
    print(f"Current Working Directory after moving back: {os.getcwd()}")
    print("="*50)
                
except pd.errors.EmptyDataError:
    print(f"The file is empty.")

print("******** video collection is DONE ********")

### keep track of the execution time
end_time = time.perf_counter()
execution_time_seconds = end_time - start_time
### convert the execution time from seconds to hours, minutes, and seconds
hours = execution_time_seconds // 3600
minutes = (execution_time_seconds % 3600) // 60
seconds = execution_time_seconds % 60

print(f"The script took {int(hours)} hours, {int(minutes)} minutes and {seconds:.2f} seconds to complete.")

#the dataframe will have a new column = tiktokurl
df.to_csv("FILENAME.csv",index=False)
            