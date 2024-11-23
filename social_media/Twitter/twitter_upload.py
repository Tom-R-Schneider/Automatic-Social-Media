from twitter.account import Account
import json
import os

credentials_path = os.path.join(os.getcwd(), 'social_media', 'Twitter', "client_secrets.json")
content_path = os.path.join(os.getcwd(), 'create_content', 'created_content')

with open(credentials_path, 'r') as file:
    credentials = json.load(file)
account = Account(cookies=credentials["cookies_path"])

def start_upload(upload_data):
    vid_content_path = os.path.join(content_path, 'videos', upload_data["post_id"] + '_vid.mp4')
    try:
        account.schedule_tweet(upload_data["post_title"], upload_data["upload_datetimeiso"].replace("T", " ")[:-3], media=[{'media': vid_content_path, 'alt': upload_data["post_id"]}])
        return True
    except(): return False 