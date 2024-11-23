import sys
import os
import json
from datetime import date

sys.path.append(os.getcwd())

from social_media.Youtube import youtube
from social_media.Tiktok import tiktok
from social_media.Facebook import facebook
from social_media.Instagram import instagram
from social_media.Twitter import twitter_upload


content_path = os.path.join(os.getcwd(), 'create_content', 'created_content')
content_file_path = os.path.join(content_path, 'content_data.json')

def start_upload_process():
    if os.path.isfile(content_file_path):
        with open(content_file_path) as f:
            content_json = json.load(f)
    
    upload_cap_counter = 0
    for post_date in content_json:
        if date.fromisoformat(post_date) < date.today() or content_json[post_date]["uploaded_all"] == True: continue
        upload_cap_counter += 1
        for upload_type in content_json[post_date]["uploaded"]:
            if upload_type == True: continue

            match upload_type:
                case "youtube": content_json[post_date]["uploaded"][upload_type] = youtube.start_upload(content_json[post_date]["content"])
                case "tiktok": content_json[post_date]["uploaded"][upload_type] = tiktok.start_upload(content_json[post_date]["content"])
                case "facebook": content_json[post_date]["uploaded"][upload_type] = facebook.start_upload(content_json[post_date]["content"])
                case "instagram": content_json[post_date]["uploaded"][upload_type] = instagram.start_upload(content_json[post_date]["content"])
                case "twitter": content_json[post_date]["uploaded"][upload_type] = twitter_upload.start_upload(content_json[post_date]["content"])

        upload_all_check = True
        for upload_type in content_json[post_date]["uploaded"]:
            if upload_type == True: continue
            upload_all_check = False
        
        content_json[post_date]["uploaded_all"] = upload_all_check

        if upload_cap_counter == 20: break