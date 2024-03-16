from requests_oauthlib import OAuth1Session
import random
import logging
from datetime import datetime
import requests
import os
import subprocess

# Set up logging
logging.basicConfig(filename='smugmug_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')

# Replace these with your actual credentials
API_KEY = ''
API_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

# The user's nickname on SmugMug
user_nickname = 'username'

# Get and save the image from a URL
def get_and_save_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_filename = "temp_image.jpg"  # Or any desired name
        with open(image_filename, 'wb') as f:
            f.write(response.content)
        return os.path.abspath(image_filename)  # Return full path
    else:
        return None  # Handle error if image download fails

# Creating an OAuth1Session with your credentials
oauth = OAuth1Session(API_KEY, client_secret=API_SECRET, resource_owner_key=ACCESS_TOKEN, resource_owner_secret=ACCESS_TOKEN_SECRET)

# Base URL for the SmugMug API
base_url = 'https://api.smugmug.com/api/v2/user/'

# Initialize a list to store all albums
all_albums = []

# Album exclusion list (can be extended with more strings to exclude)
exclusions = ["Automatic-iOS-Uploads"]

try:
    # Initial request to get the first page of albums
    response = oauth.get(f'{base_url}{user_nickname}!albums', headers={'Accept': 'application/json'})
    data = response.json()
    albums = data['Response']['Album']

    # Loop through all pages and collect albums if more pages are available
    next_page = data['Response'].get('Pages', {}).get('NextPage')
    while next_page:
        response = oauth.get(f'https://api.smugmug.com{next_page}', headers={'Accept': 'application/json'})
        data = response.json()
        albums.extend(data['Response']['Album'])
        next_page = data['Response'].get('Pages', {}).get('NextPage')

    # Filter albums based on exclusions
    filtered_albums = [album for album in albums if not any(excl in album['WebUri'] for excl in exclusions)]

    # Select a random album from the filtered list
    if filtered_albums:
        random_album = random.choice(filtered_albums)
        album_url = random_album['WebUri']
        album_name = random_album['Name']
    else:
        raise ValueError("No albums available after applying exclusions.")

    # Get all images within the selected album
    album_key = random_album['Uri'].split('/')[-1]
    response = oauth.get(f'https://api.smugmug.com/api/v2/album/{album_key}!images', headers={'Accept': 'application/json'})
    data = response.json()
    images = data['Response']['AlbumImage']

    # Select a random image from the album
    if images:
        random_image = random.choice(images)
        image_key = random_image['ImageKey']

        # Fetching ImageSizeDetails for the selected image
        response = oauth.get(f'https://api.smugmug.com/api/v2/image/{image_key}!sizedetails', headers={'Accept': 'application/json'})
        data = response.json()
        original_image_url = data['Response']['ImageSizeDetails']['ImageSizeOriginal']['Url']

        # Construct output message
        output = (f"Album: {album_name}\n"
                  f"Album URL: {album_url}\n"
                  f"Image Title: {random_image.get('Title', 'No title')}\n"
                  f"FileName: {random_image['FileName']}\n"
                  f"Caption: {random_image.get('Caption', 'No caption')}\n"
                  f"ImageSizeOriginal URL: {original_image_url}")

        print(output)
        logging.info(output)
    else:
        raise ValueError("No images found in the selected album.")

except Exception as e:
    error_message = f"An error occurred: {e}"
    print(error_message)
    logging.error(error_message)

image_path = get_and_save_image(original_image_url)

if image_path:
    # Call the AppleScript
    print(f"Trying to send via Apple Script")
    result = subprocess.run(["osascript", "/Users/username/Pictures/send_to_twinkle_turtles.scpt"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if result.returncode != 0:
        print(f"AppleScript Error: {result.stderr.decode('utf-8')}")
    
    #Don't bother removing the temporary file, it's overwritten above
    #os.remove(image_path) # Delete the temporary image file
else:
    print("Error downloading image.")

print(f"{image_path}")
