import requests
from bs4 import BeautifulSoup
import json
import sys
import os
from epitran import Epitran

sys.path.append(os.getcwd())
from utils.enums import WORD_TYPE

epi = Epitran('deu-Latn')


def get_specific_word_data(word):
    url = 'https://www.duden.de/rechtschreibung/' + word.replace("ä", "ae").replace("ü", "ue").replace("ö", "oe").replace("ß", "sz")
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    word_details = soup.find_all("dd", {"class": "tuple__val"})
    word_type = word_details[0].contents[0]
    word_data = {
        "word": word,
        "word_type": word_type
    }

    for word_type_id in WORD_TYPE:
        if word_type_id.value in word_type:
            word_data["word_type_id"] = word_type_id.value
            break

    word_data["word_sep"] = get_word_seperation(word, word_details)
    word_data["pronounciation"] = epi.transliterate(word)
    print(word_data["pronounciation"])
    word_data["url"] = url
    return word_data

def get_word_seperation(word, word_details):
    for detail in word_details:
        word_sep = detail.contents[0]
        if word_sep.replace("|", "") == word:
            break
    return word_sep        

word_list = ["gehen", "grün", "schnell", "Haus", "Tier", "aufgehen", "essen"]
data = []
for word in word_list:
    data.append(get_specific_word_data(word))


with open("test_data.json", "w") as f:
    json_object = json.dumps(data, indent=4)
    f.write(json_object)