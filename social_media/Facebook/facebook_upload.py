import json
import os
import facebook as fb
from datetime import datetime
import time


credentials_path = os.path.join(os.getcwd(), 'social_media', 'Facebook', "client_secrets.json")
content_path = os.path.join(os.getcwd(), 'create_content', 'created_content')

with open(credentials_path, 'r') as file:
    credentials = json.load(file)

fb_page = fb.GraphAPI(credentials["access_token"])

def start_upload(upload_data):
    img_content_path = os.path.join(content_path, 'images', upload_data["post_id"] + '_img.png')
    post = fb_page.put_photo(open(img_content_path, "rb"), message=upload_data["post_title"], published= False, unpublished_content_type= "SCHEDULED", scheduled_publish_time= int(time.mktime(datetime.fromisoformat(upload_data["upload_datetimeiso"]).timetuple())))
    try: 
        if post["id"] != "": return True
        return False
    except KeyError: return False
