import json
import pandas as pd
import re

file = "youtube_videos.json"
data = None
with open(file, 'r') as f:
    data = json.load(f)

dataJSON = None
with open("data.json", 'r') as f:
    dataJSON = json.load(f)

print("Starting...\n")
video_stats = data

def remove_hashtags(input_string):
    result_string = re.sub(r'\#\w+', '', input_string)
    return result_string

JSONdict = dataJSON

def bossIsNotInDataJSON(game, boss):
    if game in dataJSON.keys():
        if boss in dataJSON[game].keys():
            return False
    return True

def isGameInList(game):
    for item in JSONdict:
        if item == game:
            return True
    return False

def parseTitle(title):
    hyphen_index = title.find('-')
    if hyphen_index == -1:
        return title
    else:
        return title[:hyphen_index-1]

def parseVidTitle(title):
    hyphen_index = title.find('-')
    if hyphen_index == -1:
        return title
    else:
        return title[hyphen_index+2:]

for vid in video_stats:
    if vid["snippet"].get("title") is not None:
        title = remove_hashtags(vid["snippet"]["title"])
    else:
        continue

    img = vid['snippet']['thumbnails']['standard']['url']
    game = parseTitle(title)
    boss = parseVidTitle(title)
    embedSRC = f'https://www.youtube.com/embed/{vid['id']}'

    info = {}
    info['game'] = game
    info['boss'] = boss
    info['img'] = img
    info['embedSRC'] = embedSRC

    if bossIsNotInDataJSON(game, boss):
        print("Adding " + boss + " to " + game)
        if isGameInList(game):
            JSONdict[game].update({boss: info})
        else:
            JSONdict[game] = {}
            JSONdict[game].update({boss: info})

JSONOBJ = json.dumps(JSONdict, indent=4)
with open("data.json", "w") as file:
    file.write(JSONOBJ)

print("Done")