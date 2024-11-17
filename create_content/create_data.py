from datetime import date, datetime, timedelta
import os
import sys
import json
import requests

sys.path.append(os.getcwd())
from utils.enums import VIDEO_TYPE




def create_folder_structure():

    content_path = os.path.join(os.getcwd(), 'create_content', 'created_content')
    file_path = os.path.join(content_path, 'date_data.json')
    days_json = {}

    if not os.path.isdir(content_path):
        os.makedirs(content_path)

    if not os.path.isdir(os.path.join(content_path, 'images')):
        os.makedirs(os.path.join(content_path, 'images'))

    loop_date = date.today()   
    date_cap = loop_date + timedelta(days = 1400)
    not_at_date_cap = True

    while not_at_date_cap:
        iso_date = loop_date.isoformat()
        if not iso_date in days_json:
            days_json[iso_date] = {
                'iso_weekday': loop_date.isoweekday(),
                'content': []
            }
        loop_date += timedelta(days = 1)
        if loop_date == date_cap: not_at_date_cap = False

    json_object = json.dumps(days_json, indent=4)
    with open(file_path, "w") as outfile:
        outfile.write(json_object)



def load_word_info_from_duden(word):     
    contents = requests.get("https://www.duden.de/rechtschreibung/" + word)

def load_word_list_into_json():

    date_file_path = os.path.join(os.getcwd(), 'create_content', 'created_content', 'date_data.json')
    with open(date_file_path, "r") as f:
        date_json = json.load(f)
    
    new_word_path = os.path.join(os.getcwd(), 'create_content', 'lists', 'word_lists', 'new_words.txt')
    used_word_path = os.path.join(os.getcwd(), 'create_content', 'lists', 'word_lists', 'used_words.txt')

    new_words_file = open(new_word_path)
    new_words = [line.rstrip('\n') for line in new_words_file]
    new_words_file.close()

    newly_used_words = []

    for post_date in date_json:
        data = date_json[post_date]["content"]
        if len(new_words) > 0: 
            post_id = post_date + "_" + enums.VIDEO_TYPE.WORD
            if not post_id in date_json[post_date]["content"]:
                data.append({
                    "post_id": post_id,
                    "post_type": VIDEO_TYPE.WORD,
                    "word": new_words[0],
                    "word_type": "",
                    "image_id": post_date + 'IMG_' + enums.VIDEO_TYPE.WORD,
                    "content_created": False
                })
                newly_used_words.append(new_words.pop(0))
                
            date_json[post_date]["content"].append(data)

    with open(used_word_path, "a") as f:
        for line in newly_used_words:
            f.write(f"{line}\n")

    with open(date_file_path, "w") as f:
        json_object = json.dumps(date_json, indent=4)
        f.write(json_object)

    with open(new_word_path, "w") as f:
        json_object = json.dumps(new_words, indent=4)
        f.write(json_object)
            
# create_folder_structure()
# load_word_info_from_duden("Hallo")
load_word_list_into_json()