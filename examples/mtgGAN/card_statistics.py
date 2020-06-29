import json
import os

"""
Goal: quick access to basic card statistics (e.g. X% of cards are type ABC)
"""


def load_master_bulk(fpath, verbose=False):
    # read MASTER_BULK json -- a DICT with 3 keys:
    #   'object'   -> list
    #   'has_more' -> False
    #   'data'     -> dict of download info
    # stores information on the cards download
    with open(fpath, encoding="utf8") as f:
        json_master_bulk = json.load(f)
    if verbose:
        print("Loaded: MASTER_BULK.json; Type:%s" % type(json_master_bulk))
        print("MASTER_BULK -- keys:\n",  json_master_bulk.keys())
        print(json_master_bulk['object'])
        print(json_master_bulk['has_more'])
        print(json_master_bulk['data'], '\n')
    return json_master_bulk


def load_unique_artwork(fpath, verbose=False):
    # read UNIQUE_ARTWORK json (a LIST of 26656 DICTs each with 47-62 keys)
    with open(fpath, encoding="utf8") as f:
        json_unique_dicts = json.load(f)
    # inspect UNIQUE_ARTWORK json
    if verbose:
        print("Loaded: UNIQUE_ARTWORK.json; Type:%s" % type(json_unique_dicts))
        print("Length UNIQUE_ARTWORK: %d" % len(json_unique_dicts))
        print("First element UNIQUE_ARTWORK -- keys:\n",  json_unique_dicts[0].keys())
        json_unique_dicts_keycounts = [len(elem) for elem in json_unique_dicts]
        print("Min, max # of keys:", min(json_unique_dicts_keycounts), max(json_unique_dicts_keycounts), '\n')
    return json_unique_dicts



if __name__ == '__main__':
    bulk_dir = "Bulk_JSON"
    path_master_bulk = bulk_dir + os.sep + "MASTER_BULK.json"
    path_unique_artwork = bulk_dir + os.sep + "UNIQUE_ARTWORK.json"

    load_master_bulk(path_master_bulk, verbose=True)
    load_unique_artwork(path_unique_artwork, verbose=True)
