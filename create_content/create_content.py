from datetime import date, datetime
import os
import json

def create_folder_structure():

    content_path = os.path.join(os.getcwd(), 'create_content', 'created_content')
    if not (os.path.isdir(content_path)):
        os.makedirs(content_path)
        
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    year_cap = year + 4
    for y in range(year, year_cap):
        year_path = os.path.join(content_path, str(y))
        images_path = os.path.join(year_path, 'images')
        if not (os.path.isdir(year_path)):
            os.makedirs(year_path)
        if not (os.path.isdir(images_path)):
            os.makedirs(images_path)
        
        for m in range(month, 13):
            month_path = os.path.join(year_path, str(m) + '.json')
            if not (os.path.isfile(month_path)):
                days_json = {}
                for d in range(day, 32):
                    try:
                        new_date = datetime(y,m,d)
                        new_date.isoweekday()
                        days_json[str(d)] = {
                            'iso_weekday': new_date.isoweekday(),
                            'content': []
                        }
                    except ValueError:
                        break

                json_object = json.dumps(days_json, indent=4)
                with open(month_path, "x") as outfile:
                    outfile.write(json_object)

                day = 1
        month = 1

        


create_folder_structure()