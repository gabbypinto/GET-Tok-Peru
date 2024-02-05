"""
author: Gabriela Pinto
date: Feb 4, 2024

This script extract the audio from the video and uses Whisper to generate the transcript
"""

import whisper
import subprocess
import ssl
import pandas as pd
import time


def extract_audio_from_video(video_path, audio_path):
    """
        Extracts the audio from the video, generate the mp3 file

        Parameters:
        str: 
        video_path = path to your mp4/video file
        audio_path = path to the mp3/audio file

        Returns:
        boolean: True if the audio was succesfully extracted, False if the operation was unsuccessfully
    """

    command = ["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error processing video file {video_path}: {e}")
        return False  
    return True

def transcribe_audio(file_path):
    """
       Calls Whisper to transcribe the audio

        Parameters:
        str: path to the mp3/audio file

        Returns:
        str: the transcript/text
    """

    # Transcribe the audio
    result = model.transcribe(file_path)

    # Return the transcribed text
    return result["text"]


def gen_audio_file(row,videos_folder_path,audio_folder_path,total_rows):
    """
       Calls Whisper to transcribe the audio

        Parameters:
        str: path to the mp3/audio file

        Returns:
        str: the transcript/text
    """
    start_row_time = time.time()

    vid_id = str(row['id'])
    vid_user = row['username']
    video_file_name = "@"+vid_user+"_video_"+vid_id+".mp4"
    audio_file_name = "@"+vid_user+"_video_"+vid_id+".mp3"

    #the output/ audio file that will be created
    audio_path = audio_folder_path+"/"+audio_file_name  

    #the input/ video file 
    videos_path = videos_folder_path+video_file_name

    extractionCompleted=extract_audio_from_video(videos_path,audio_path)
    if extractionCompleted == True:
        whisper_transcript = transcribe_audio(audio_path)

        end_row_time = time.time()  # Time after processing the row
        print(f"Row {row.name + 1}/{total_rows} processing time: {end_row_time - start_row_time:.4f} seconds\n")

        invalidFormat = False
        return pd.Series([audio_path,whisper_transcript,invalidFormat])
    else:
        invalidFormat = True
        return pd.Series([None,None,invalidFormat])



def process_file(file_path_csv):
    """
        Extract the audio file from each video file and calls Whisper to generate the transcripts 

        Parameters:
        str: path to your csv file contains Tiktok metadata and tiktokurl

        Returns:
        None, new csv file is generated with the transcript
    """
    start_process_time = time.time()  # Start time of the process

    #set your directories
    audio_dir = "INSERT FILE PATH TO YOUR DIRECTORY WHERE AUDIO FILES WILL BE STORED" #create a directory where your audio files will be stored
    cur_videos_folder = "INSERT FILE PATH TO YOUR DIRECTORY WITH VIDEO FILES" #set the path to the directory where you have your video/mp4 files

    #read your csv file
    df = pd.read_csv(file_path_csv)
    total_rows = len(df)

    # Process the DataFrame
    df[['audio_file_path', 'whisper_voice_to_text','invalid_format']] = df.apply(gen_audio_file, axis=1, args=(cur_videos_folder, audio_dir, total_rows))

    # Save the processed DataFrame
    output_path = "FILENAME.csv"
    df.to_csv(output_path,index=False)
        
    end_process_time = time.time()
    print(f"Processing of file {file_path_csv} took {end_process_time - start_process_time:.2f} seconds.\n")
    print("="*100)



# Load the Whisper model
model = whisper.load_model("large-v3")

# Temporary workaround for SSL certificate issue
ssl._create_default_https_context = ssl._create_unverified_context

#insert the name of your file
process_file('FILENAME.csv')
