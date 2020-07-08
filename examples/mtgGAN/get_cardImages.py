import json
import os
import requests as req
import sys
import time
from collections import Counter
from glob import glob

def get_json(json_path):

    # get updated master bulk JSON file if it isn't already in directory
    if not os.path.exists(json_path):
        os.makedirs(json_path)
    else:
        print("JSON files exist\n")

    if not os.path.exists(json_path + "MASTER_BULK.json") and not os.path.exists(json_path + "UNIQUE_ARTWORK.json"):
        master_bulk_url = "https://api.scryfall.com/bulk-data"
        master_bulk = req.get(master_bulk_url, allow_redirects=True)
        open(bulkDir + "MASTER_BULK.json", 'wb').write(master_bulk.content)

        # now get json for unique art cards
        f = open(json_path + "MASTER_BULK.json")
        master_json_dicts = json.load(f)

        for object in master_json_dicts['data']:
            if object['name'] == 'Unique Artwork':
                unique_bulk_url = object['download_uri']

        unique_artwork_bulk = req.get(unique_bulk_url, allow_redirects=True)
        open(json_path + "UNIQUE_ARTWORK.json", 'wb').write(unique_artwork_bulk.content)

def get_images_sort_creatures(json_file, working_directory):

    primary_creature_types = []
    primary_creature_indicies = []

    files_present = []
    pattern = "*.jpg"
    num_cards_downloaded = 0

    for i, card in enumerate(json_file):
        type = card['type_line']
        if "Creature" in type and "Token" not in type:
            type_seg = type.strip().split()
            if '—' in type_seg:
                primary_type = type_seg[type_seg.index('—')+1]
                primary_creature_types.append(primary_type)
                primary_creature_indicies.append(i)

    # take creature types and download images into respective folders (respecting API call frequency limits)
    types_to_count = Counter(primary_creature_types)
    main_types = types_to_count.most_common(10)

    creature_imageDir = working_directory + '/Images/Creatures/'

    if not os.path.exists(creature_imageDir):
        os.makedirs(creature_imageDir)

    for dir, _, _ in os.walk(creature_imageDir):
        files_present.extend(glob(os.path.join(dir, pattern)))

    print("--downloading top 10 most abundant creature type images--\n")
    for ele in main_types:
        type = ele[0]
        print("\ndownloading images for " + str(type) + ':\n')
        type_path = creature_imageDir + os.sep + str(type) + os.sep

        indicies_of_type = [i for i, x in enumerate(primary_creature_types) if x ==type]
        indicies_of_json = [primary_creature_indicies[i] for i in indicies_of_type]

        if not os.path.exists(type_path):
            os.makedirs(type_path)

        #download images into folder with 100ms delay between API requests
        num_files = len(indicies_of_json)

        for i, index in enumerate(indicies_of_json):
            id = json_file[index]["id"]
            filename = id + ".jpg"

            if not any(filename in s for s in files_present):
                if "image_uris" in json_file[index].keys():
                    image = req.get(json_file[index]["image_uris"]["art_crop"], allow_redirects=True)
                    open(type_path + str(json_file[index]["id"]) + ".jpg", 'wb').write(image.content)
                    sys.stdout.write("\r" + str(i) + '/' + str(num_files))
                    sys.stdout.flush()
                    time.sleep(0.1)

def get_images_sort_colours(json_file, working_directory):

    print("\n--downloading images and filing based on colour (will take >45 mins)--" + ':\n')
    print("Progress" + ':\n')
    colours_imageDir = working_directory + '/Images/Colours/'
    colours = {'U':'Blue', 'B':'Black', 'R':'Red', 'G':'Green', 'W':'White'}

    num_files = len(json_file)
    files_present = []
    pattern = "*.jpg"
    num_cards_downloaded = 0

    if not os.path.exists(colours_imageDir):
        os.makedirs(colours_imageDir)

    for dir,_,_ in os.walk(colours_imageDir):
        files_present.extend(glob(os.path.join(dir,pattern)))

    num_cards_downloaded = len(files_present)

    #download all images and sort by colour
    for card in json_file:
        colours_present = card["color_identity"]
        id = card["id"]
        type = card['type_line']
        filename = id + ".jpg"

        if not any(filename in s for s in files_present):
            if "image_uris" in card.keys():

                #if a land place in its own folder (colour isn't really well defined)
                if "Land" in type:
                    path = colours_imageDir + str("Land") + os.sep

                #if a multicoloured card place in separate folder
                elif len(colours_present) >1:
                    path = colours_imageDir  + str("Multicoloured") + os.sep

                #if no colours present this is a colourless card
                elif len(colours_present)==0:
                    path = colours_imageDir + str("Colourless") + os.sep

                else:
                    path = colours_imageDir  + str(colours[colours_present[0]]) + os.sep

                if not os.path.exists(path):
                    os.makedirs(path)

                image = req.get(card["image_uris"]["art_crop"], allow_redirects=True)
                open(path + str(card["id"]) + ".jpg", 'wb').write(image.content)
                sys.stdout.write("\r" + str(num_cards_downloaded) + '/' + str(num_files))
                sys.stdout.flush()
                time.sleep(0.1)

            num_cards_downloaded += 1

def main():
    #define current working directory
    currDir = os.path.dirname(os.path.realpath(__file__))

    #define where json files will live
    bulkDir = currDir + os.sep + "Bulk_JSON" + os.sep

    #dowload and format JSON files
    get_json(bulkDir)

    #open unique artwork json file
    with open(bulkDir + "UNIQUE_ARTWORK.json", encoding="utf8") as json_file:
        unique_json_dicts = json.load(json_file)

    #get images, choosing colours for example here
    get_images_sort_colours(unique_json_dicts, currDir)
    get_images_sort_creatures(unique_json_dicts, currDir)

if __name__=="__main__":
    main()
