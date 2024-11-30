from datetime import date, datetime, timedelta
import os
import sys
import json

sys.path.append(os.getcwd())
from utils.enums import VIDEO_TYPE
import create_content.content_automations.duden_word as duden




def create_folder_structure():

    content_path = os.path.join(os.getcwd(), 'create_content', 'created_content')
    file_path = os.path.join(content_path, 'date_data.json')
    days_json = {}

    if os.path.isfile(file_path):
        with open(file_path) as f:
            days_json = json.load(f)

    if not os.path.isdir(content_path):
        os.makedirs(content_path)

    if not os.path.isdir(os.path.join(content_path, 'images')):
        os.makedirs(os.path.join(content_path, 'images'))

    if not os.path.isdir(os.path.join(content_path, 'videos')):
        os.makedirs(os.path.join(content_path, 'videos'))

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


def load_word_list_into_json():
    date_file_path = os.path.join(os.getcwd(), 'create_content', 'created_content', 'date_data.json')
    new_word_path = os.path.join(os.getcwd(), 'create_content', 'lists', 'word_lists', 'new_words.txt')
    used_word_path = os.path.join(os.getcwd(), 'create_content', 'lists', 'word_lists', 'used_words.txt')

    with open(date_file_path, "r") as f:
        date_json = json.load(f)

    with open (new_word_path, "r") as new_words_file:
        new_words = [line.rstrip('\n') for line in new_words_file]

    newly_used_words = []

    for post_date in date_json:
        if date.fromisoformat(post_date) < date.today():
            continue

        data = date_json[post_date]["content"]
        if len(new_words) > 0: 
            post_id = post_date + "_" + VIDEO_TYPE.WORD.ID_SUFFIX
            if not any(obj['post_id'] == post_id for obj in date_json[post_date]["content"]):
                data.append({
                    "post_id": post_id,
                    "post_type": VIDEO_TYPE.WORD.ID_SUFFIX,
                    "word": new_words[0],
                    "content_details": duden.get_specific_word_data(new_words[0]),
                    "ready_for_content": False,
                    "content_created": False
                })
                newly_used_words.append(new_words.pop(0))
                
            # date_json[post_date]["content"].append(data)

    with open(used_word_path, "a") as f:
        for line in newly_used_words:
            f.write(f"{line}\n")

    with open(date_file_path, "w") as f:
        json_object = json.dumps(date_json, indent=4)
        f.write(json_object)

    with open(new_word_path, "w") as f:
        for line in new_words:
            f.write(f"{line}\n")
            

create_folder_structure()
load_word_list_into_json()

def start_create_data():
    create_folder_structure()
    load_word_list_into_json()