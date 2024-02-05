"""
author: Gabriela Pinto
date: Feb 4, 2024
"""

def is_mp4_file(file_path):
    """
        Check if the video is a valid mp4

        Parameters:
        str: file path to the mp4 file
        
        Returns:
        boolean: True if the mp4 is valid, False if its not
    """
    try:
        with open(file_path, 'rb') as file:
            header = file.read(12)
            # Check for MP4 signature (ftyp box)
            return header[4:8] == b'ftyp'
    except IOError:
        return False

is_mp4_file('FILE PATH TO VIDEO.mp4')