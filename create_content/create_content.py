from datetime import date, datetime, timedelta
import os
import json
import requests


def create_folder_structure():

    content_path = os.path.join(os.getcwd(), 'create_content', 'created_content')
    file_path = os.path.join(content_path, 'date_data.json')
    days_json = {}

    if not os.path.isdir(content_path):
        os.makedirs(content_path)

    if not os.path.isdir(os.path.join(content_path, 'images')):
        os.makedirs(os.path.join(content_path, 'images'))

    loop_date = date.today()   

    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            days_json = json.load(f)
            loop_date = date.fromisoformat(list(days_json)[-1])
        
    date_cap = loop_date + timedelta(days = 1400)

    while True:
        if loop_date == date_cap: break
        days_json[loop_date.isoformat()] = {
            'iso_weekday': loop_date.isoweekday(),
            'content': []
        }
        loop_date += timedelta(days = 1)

    json_object = json.dumps(days_json, indent=4)
    with open(file_path, "w") as outfile:
        outfile.write(json_object)



def load_word_info_from_duden(word):     
    contents = requests.get("https://www.duden.de/rechtschreibung/" + word)

def load_word_list_into_json():
    with open(os.path.join(os.getcwd(), 'create_content', 'lists', 'word_lists', "config.json")) as f:
        configs = json.load(f)

    date_file_path = os.path.join(os.getcwd(), 'create_content', 'created_content', 'date_data.json')
    with open(date_file_path, "r") as f:
        date_json = json.load(f)
    
    new_word_path = os.path.join(os.getcwd(), 'create_content', 'lists', 'word_lists', 'new_words.txt')
    used_word_path = os.path.join(os.getcwd(), 'create_content', 'lists', 'word_lists', 'used_words.txt')

    new_words_file = open(new_word_path)
    new_words = [line.rstrip('\n') for line in new_words_file]
    new_words_file.close()

    newly_used_words = []
    if configs["earliest_day_no_data"] != "": 
        loop_date = date.fromisoformat(configs["earliest_day_no_data"])
    else:
        loop_date = date.today()

    still_available = {
        "word": True
    }

    still_going = True
    while(still_going):
        post_this_day = False
        for post_type in still_available:
            if still_available[post_type]:
                post_this_day = True
                
                match post_type:
                    case "word":
                        data = {
                            "post_type": "word",
                            "word": new_words[0],
                            "word_type": "",
                            "image_id"
                            "approved": False,
                            "all_uploaded": False,
                            "uploaded": {
                                "youtube": False
                            }

                        }
                        newly_used_words.append(new_words.pop(0))
                        if len(new_words) == 0: 
                            still_available[post_type] = False
                            configs["earliest_day_no_data"] = (loop_date + timedelta(days = 1)).isoformat()

                date_json[loop_date.isoformat()]["content"].append(data)

        still_going = post_this_day
        loop_date += timedelta(days = 1)

    with open(used_word_path, "a") as f:
        for line in newly_used_words:
            f.write(f"{line}\n")

    with open(os.path.join(os.getcwd(), 'create_content', 'lists', 'word_lists', "config.json"), "w") as f:
        json.dump(configs, f)
    
    with open(date_file_path, "w") as f:
        json_object = json.dumps(date_json, indent=4)
        f.write(json_object)

    with open(new_word_path, "r+") as f:
        f.seek(0)  
        f.truncate()  
            
# create_folder_structure()
# load_word_info_from_duden("Hallo")
load_word_list_into_json()