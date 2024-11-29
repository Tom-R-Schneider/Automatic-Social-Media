import json
import os
import datetime
import time
import requests


credentials_path = os.path.join(os.getcwd(), 'social_media', 'Instagram', "client_secrets.json")
content_path = os.path.join(os.getcwd(), 'create_content', 'created_content')

with open(credentials_path, 'r') as file:
    credentials = json.load(file)

# Note that instagram always has to upload after facebook as we use the facebook image host for instagram 
# as instagram doesn't allow local file upload
def start_upload(upload_data):
    # TODO: Fetch/Build image url for facebook hosted image
    image_url = "TODO"
    url = "https://graph.facebook.com/v21.0/" + credentials["account_id"] + "/media"
    payload = json.dumps({
    "url": image_url,
    "access_token": credentials["access_token"],
    "message": upload_data["post_title"],
    "published": False,
    "scheduled_publish_time": upload_data["upload_datetimeiso"]
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return True