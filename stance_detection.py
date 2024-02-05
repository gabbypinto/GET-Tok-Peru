"""
author: Gabriela Pinto
date: Feb 4, 2024

This scripts using zero-shot prompting to classify the stance expressed given the 
transcript, video description, and one frame from the inputted video
"""

import pandas as pd
import cv2  
import base64
from openai import OpenAI
import requests
import pandas as pd


OPEN_AI_KEY = "APIKEY"
client = OpenAI(api_key=OPEN_AI_KEY)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {OPEN_AI_KEY}"
}


def encode_image(image_path):
    """
        Encode the image

        Parameters:
        str: file path to the image/screenshot

        Returns:
        base64: encoded the image
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')




videoPath = "FILE PATH TO VIDEO.mp4"
screenshotPath = "FILE PATH TO GENERATED SCREENSHOT.jpg"

#generate a screenshot
cap = cv2.VideoCapture(videoPath)

#check if video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

frame_number = 50 #frame you want to read
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

ret, frame = cap.read() #read the frame
if ret:
    cv2.imwrite(screenshotPath, frame) #save the frame as an image file
else:
    print("Error: Could not read frame.")
cap.release() #release the video capture object

image_path = screenshotPath #path to your screenshot image
base64_image = encode_image(image_path) #getting the base64 string

payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text":''' 
Transcript:  INSERT TRANSCRIPT HERE
Text Displayed in the Video: INSERT VIDEO DESCRIPTION HERE
'''
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    },
    {"role": "system", 
     "content": "Based on the transcript, description of what is occurring and shown in the video, and a frame from the video, classify the input as 'support' if the input shows support for Pedro Castillo as President of Peru, or as 'no support' if the input does not show support for Pedro Castillo as President of Peru, or as 'neutral' if input is neutral"
    }
  ],
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
print(response.json())