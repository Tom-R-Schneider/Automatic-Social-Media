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
        "example_sentence": "",
        "word_type_raw": word_type
    }

    word_data["word_sep"] = get_word_seperation(word, word_details)
    word_data["pronounciation"] = epi.transliterate(word)

    if WORD_TYPE.NOUN.value in word_data["word_type_raw"]:
        word_data["word_type_id"] = WORD_TYPE.NOUN.value
        word_data["genus"] = word_data["word_type_raw"].split(", ")[1]
        match word_data["genus"]:
            case "Neutrum":
                word_data["article"] = 'das'
            case "maskulin":
                word_data["article"] = 'der'
            case "feminin":
                word_data["article"] = 'die'

        site_ps = soup.find_all("p")
        for site_p in site_ps:
            if "Genitiv" in site_p.contents[0]:
                # Content example: 'das Haus; Genitiv: des Hauses, Häuser'
                temp = site_p.contents[0].split("Genitiv: ")[1].split(", ")
                word_data["grammarone"] = { "value": temp[0], "label": "Genitiv" }
                word_data["grammartwo"] = { "value": temp[1].replace("Plural: ", ""), "label": "Plural" }
                break

    elif WORD_TYPE.ADJECTIVE.value in word_data["word_type_raw"]:
        word_data["word_type_id"] = WORD_TYPE.ADJECTIVE.value
        site_ps = soup.find_all("p")
        for site_p in site_ps:
            if "Steigerungsformen" in site_p.contents[0]:
                # Content example: 'Adjektiv; Steigerungsformen: stärker, stärkste'
                temp = site_p.contents[0].split("Steigerungsformen: ")[1].split(", ")
                word_data["grammarone"] = { "value": temp[0], "label": "Komperativ" }
                word_data["grammartwo"] = { "value": temp[1], "label": "Superlativ" }
                break

        if word_data.get("grammarone") is None:
            # Needs a new call for conjugation
            grammar_url = 'https://www.duden.de/deklination/adjektive/' + word.replace("ä", "ae").replace("ü", "ue").replace("ö", "oe").replace("ß", "sz")
            r = requests.get(grammar_url)
            soup = BeautifulSoup(r.content, 'html.parser')
            word_details = soup.find_all("li", {"class": "accordion__item"})
            for idx, detail in enumerate(word_details):
                if "Komparativ" in detail.contents[0]:
                    word_data["grammarone"] = { "value": word_details[idx + 1].contents[0], "label": "Komperativ" }
                if "Superlativ" in detail.contents[0]:
                    word_data["grammartwo"] = { "value": word_details[idx + 1].contents[0], "label": "Superlativ" }

    elif WORD_TYPE.VERB.value in word_data["word_type_raw"]:
        word_data["word_type_id"] = WORD_TYPE.VERB.value
        word_data["verb_type"] = word_data["word_type_raw"]
        site_ps = soup.find_all("p")
        for site_p in site_ps:
            if ("hat" in site_p.contents[0] or "ist" in site_p.contents[0]) and ", " in site_p.contents[0]:
                # Content example: 'schläft, schlief, hat geschlafen'
                temp = site_p.contents[0].split(", ")
                word_data["grammarone"] = { "value": "er " + temp[0], "label": "Präsens" }
                word_data["grammartwo"] = { "value": "sie " + temp[1], "label": "Präteritum" }
                word_data["grammarthree"] = { "value": "es " + temp[2], "label": "Perfekt" }
                break
        if word_data.get("grammarone") is None:
            # Needs a new call for conjugation
            grammar_url = 'https://www.duden.de/konjugation/' + word.replace("ä", "ae").replace("ü", "ue").replace("ö", "oe").replace("ß", "sz")
            r = requests.get(grammar_url)
            soup = BeautifulSoup(r.content, 'html.parser')
            word_details = soup.find_all("li", {"class": "accordion__item"})
            for idx, detail in enumerate(word_details):
                if "Präsens" in detail.contents[0] and word_data.get("grammarone") is None:
                    word_data["grammarone"] = { "value": "er " + word_details[idx + 3].contents[0], "label": "Präsens" }
                if "Präteritum" in detail.contents[0] and word_data.get("grammartwo") is None:
                    word_data["grammartwo"] = { "value": "sie " + word_details[idx + 3].contents[0], "label": "Präteritum" }
                if "Perfekt" in detail.contents[0] and word_data.get("grammarthree") is None:
                    word_data["grammarthree"] = { "value": "es " + word_details[idx + 3].contents[0], "label": "Perfekt" }
    else:
        # Only allow noun/adjektive/verb for now
        return
    word_data["url"] = url
    return word_data

def get_word_seperation(word, word_details):
    for detail in word_details:
        word_sep = detail.contents[0]
        if word_sep.replace("|", "") == word:
            break
    return word_sep        

# word_list = ["gehen", "stark", "schnell", "Haus", "Tier", "aufgehen", "essen", "schlafen"]
# data = []
# for word in word_list:
#     data.append(get_specific_word_data(word))


# with open("test_data.json", "w") as f:
#     json_object = json.dumps(data, indent=4)
#     f.write(json_object)