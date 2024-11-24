from twitter.account import Account
import json
import os

credentials_path = os.path.join(os.getcwd(), 'social_media', 'Twitter', "client_secrets.json")
content_path = os.path.join(os.getcwd(), 'create_content', 'created_content')

with open(credentials_path, 'r') as file:
    credentials = json.load(file)
account = Account(cookies=credentials["cookies_path"])

def start_upload(upload_data):
    img_content_path = os.path.join(content_path, 'images', upload_data["post_id"] + '_img.png')
    tweet = account.schedule_tweet(upload_data["post_title"], upload_data["upload_datetimeiso"].replace("T", " ")[:-3], media=[{'media': img_content_path, 'alt': upload_data["post_id"]}])
    try: 
        if tweet["data"]["tweet"]["rest_id"] != "": return True
        return False
    except KeyError: return False