import sys
import os
import json
from datetime import date

sys.path.append(os.getcwd())

from social_media.Youtube import youtube


content_path = os.path.join(os.getcwd(), 'create_content', 'created_content')
content_file_path = os.path.join(content_path, 'content_data.json')

import social_media.Youtube.youtube as youtube

def start_upload_process():
    if os.path.isfile(content_file_path):
        with open(content_file_path) as f:
            content_json = json.load(f)
    
    for post_date in content_json:
        if date.fromisoformat(post_date) < date.today() or content_json[post_date]["uploaded_all"] == True: continue


        for upload_type in content_json[post_date]["uploaded"]:
            if upload_type == True: continue
            match upload_type:
                case "youtube": 
                    upload_success = youtube.start_upload(content_json[post_date]["content"])



    youtube.start_upload()