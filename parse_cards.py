"""
Builds cards.js
"""
import json
import logging
import os

CARDS_FILE = 'AllSets.json'
HEADER = """
/*
This file is auto-generated.  Do not edit by hand.
*/
"""
OUT_FILE = "cards.js"


logging.basicConfig(level=logging.DEBUG)


def fetch_card_data():
    """
    TODO:  wget this file from the interwebs (https://mtgjson.com/)
    we can check the version to see if we have the latest data already
    then, we can auto-update the addon when mtgjson updates
    """
    pass


def read_cards_file(path):
    """load json from file into dict"""
    with open(path) as data_file:
        data = json.load(data_file)
    return data


def parse_name(name):
    """card name fixes so that we get valid js"""
    # escape quotation marks
    name = name.replace('"', '\\"')
    name = name.lower()
    return name


def write_js_file(cards_dict):
    """write the data file used in the addon"""
    with open(OUT_FILE, 'w') as js_file:
        js_file.write(HEADER)
        js_file.write('var cards = {')

        for name, multiverse_id in cards_dict.items():
            name = parse_name(name)
            output = '"%s":"%s",' % (name, multiverse_id)
            logging.debug("writing %s", output)
            js_file.write(output.encode('utf-8'))

        js_file.seek(-1, os.SEEK_CUR)  # overwrite the last comma
        js_file.write('};\n')


def create_cards_dict():
    """convert the read of the cards file into a usable dictionary"""
    all_cards = read_cards_file(CARDS_FILE)
    cards_dict = {}
    for exp, info in all_cards.items():
        for card in info['cards']:
            if 'multiverseid' in card and 'name' in card:
                if card['name'] in cards_dict:
                    if card['multiverseid'] > cards_dict[card['name']]:
                        cards_dict[card['name']] = card['multiverseid']
                else:
                    cards_dict[card['name']] = card['multiverseid']
    return cards_dict


def main():
    """script entrypoint"""
    write_js_file(create_cards_dict())


main()
