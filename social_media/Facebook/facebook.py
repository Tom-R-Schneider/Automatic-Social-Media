import json
import os
import datetime
import time
import requests


credentials_path = os.path.join(os.getcwd(), 'social_media', 'Facebook', "client_secrets.json")
content_path = os.path.join(os.getcwd(), 'create_content', 'created_content')

with open(credentials_path, 'r') as file:
    credentials = json.load(file)

def start_upload(upload_data):
    # vid_content_path = os.path.join(content_path, 'videos', upload_data["post_id"] + '_vid.mp4')

    url = "https://graph.facebook.com/v21.0/" + credentials["page_id"] + "/post"
    payload = json.dumps({
    "access_token": credentials["page_access_token"],
    "message": "Testing",
    "published": "false",
    "scheduled_publish_time":  "2024-12-20T17:00:00" #upload_data["upload_datetimeiso"]
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return True


start_upload({})
