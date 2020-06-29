import json
import os
import requests as req
import sys
import time
from collections import Counter


# get updated master bulk JSON file if it isn't already in directory
currDir = os.path.dirname(os.path.realpath(__file__))
bulkDir = currDir + os.sep + "Bulk_JSON" + os.sep

if not os.path.exists(bulkDir):
    os.makedirs(bulkDir)

if not os.path.exists(bulkDir + "MASTER_BULK.json") and not os.path.exists(bulkDir + "UNIQUE_ARTWORK.json"):
    master_bulk_url = "https://api.scryfall.com/bulk-data"
    master_bulk = req.get(master_bulk_url, allow_redirects=True)
    open(bulkDir + "MASTER_BULK.json", 'wb').write(master_bulk.content)

    # now get json for unique art cards
    f = open(bulkDir + "MASTER_BULK.json")
    master_json_dicts = json.load(f)

    for object in master_json_dicts['data']:
        if object['name'] == 'Unique Artwork':
            unique_bulk_url = object['download_uri']

    unique_artwork_bulk = req.get(unique_bulk_url, allow_redirects=True)
    open(bulkDir + "UNIQUE_ARTWORK.json", 'wb').write(unique_artwork_bulk.content)

# read unique art json and print
f = open(bulkDir + "UNIQUE_ARTWORK.json", encoding="utf8")
unique_json_dicts = json.load(f)

#print(unique_json_dicts[0]["image_uris"]["art_crop"])

primary_creature_types = []
primary_creature_indicies = []

for i, card in enumerate(unique_json_dicts):
    type = card['type_line']
    if "Creature" in type and "Token" not in type:
        type_seg = type.strip().split()
        if '—' in type_seg:
            primary_type = type_seg[type_seg.index('—')+1]
            primary_creature_types.append(primary_type)
            primary_creature_indicies.append(i)

# take the top 10 most abundant creature types and download images into respective folders (respecting API call frequency limits)
types_to_count = Counter(primary_creature_types)
main_type = types_to_count.most_common(10)

imageDir = currDir + '/Images/'

if not os.path.exists(imageDir):
    os.makedirs(imageDir)

for ele in main_type:
    type = ele[0]
    print("\ndownloading images for " + str(type) + ':\n')
    type_path = imageDir + '/' + str(type) + '/'

    indicies_of_type = [i for i, x in enumerate(primary_creature_types) if x ==type]
    indicies_of_json = [primary_creature_indicies[i] for i in indicies_of_type]

    if not os.path.exists(type_path):
        os.makedirs(type_path)
    else:
        #download images into folder with 100ms delay between API requests
        num_files = len(indicies_of_json)
        for i, index in enumerate(indicies_of_json):
            if "image_uris" in unique_json_dicts[index].keys():
                image = req.get(unique_json_dicts[index]["image_uris"]["art_crop"], allow_redirects=True)
                open(type_path + str(i) + ".jpg", 'wb').write(image.content)
                sys.stdout.write("\r" + str(i) + '/' + str(num_files))
                sys.stdout.flush()
                time.sleep(0.1)
