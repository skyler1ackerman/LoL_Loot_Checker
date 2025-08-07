# Loads the existing skins frim skinGetter.py
# From the JSON files and does analysis on them
import json, csv
from pprint import pprint

# Generic function to load JSON data
def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"{filename} not found. Please run skinGetter.py first.")
    
def dict_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(data[0].keys())
        # Write data rows
        for item in data:
            writer.writerow(item.values())

# Specific functions to load champions, skins, and loot
# NOTE: None of these functions will work if the JSON files do not exist
def load_champions():
    return load_json('data/champions.json')

def load_skins():
    return load_json('data/skins.json')

def load_loot():
    return load_json('data/loot.json')

# Basic functions to check all owned champions and skins
def analyze_champions(champions):
    owned_champions = [champ for champ in champions if champ['ownership']['owned']]
    total_owned = len(owned_champions)
    print(f"Total Owned Champions: {total_owned}")
    return owned_champions

def analyze_skins(skins):
    owned_skins = [skin for skin in skins if skin['ownership']['owned']]
    total_owned = len(owned_skins)
    print(f"Total Owned Skins: {total_owned}")
    return owned_skins

# Functions to find unowned champions and skins
def unowned_skins(skins):
    unowned = [skin for skin in skins if not skin['ownership']['owned']]
    print(f"Total Unowned Skins: {len(unowned)}")
    return unowned

def unowned_champions(champions):
    unowned = [champ for champ in champions if not champ['ownership']['owned']]
    print(f"Total Unowned Champions: {len(unowned)}")
    return unowned

# Functions to map chamption IDs to champion names
# This is sometimes needed when the data only has champion IDs
def champ_id_dict_maker(champions):
    return {champ['id']: champ['name'] for champ in champions}

# Functions to find champions with owned skins and those without
# Sorts the returned dictionary by number of owned skins
def champs_with_owned_skins(champions, skins):
    champ_skin_dict = {}
    for champ in champions:
        champ_id = champ['id']
        # Also process out tha basic skins
        # (Skin has the same name as the champion)
        champ_skin_dict[champ_id] = [skin for skin in skins if skin['championId'] == champ_id
                                      and skin['ownership']['owned']
                                        and not skin['isBase']]
    # Filter out champions with no owned skins
    champ_skin_dict = {k: v for k, v in champ_skin_dict.items() if v}
    # Lastly, sort the dictionary by number of skins
    champ_skin_dict = dict(sorted(champ_skin_dict.items(), key=lambda item: len(item[1]), reverse=True))

    return champ_skin_dict

# Find champions with no owned skins
def champions_with_no_skins(champions, skins):
    champ_id_dict = champ_id_dict_maker(champions)
    champ_skin_dict = champs_with_owned_skins(champions, skins)
    no_skin_champs = {k: v for k, v in champ_id_dict.items() if k not in champ_skin_dict}
    return no_skin_champs

# Functions to get loot data
def get_all_owned_loot(loot):
    owned_loot = [item for item in loot if item['count'] >= 1]
    print(f"Total Owned Loot Items: {len(owned_loot)}")
    return owned_loot

def get_given_loot(loot, given_type):
    given_loot = [item for item in loot if item['type'] == given_type]
    return given_loot

def get_loot_skin_shards(loot):
    return get_given_loot(loot, 'SKIN_RENTAL')

def get_loot_champion_shards(loot):
    return get_given_loot(loot, 'CHAMPION_RENTAL')

       ### Other Possible Types ###
# 'CURRENCY', 'SKIN_RENTAL', 'TOURNAMENTLOGO'
#  'WARDSKIN_RENTAL', 'EMOTE', 'STATSTONE_SHARD'
#  'SKIN', 'STATSTONE', 'MATERIAL', 'WARDSKIN'
#  'CHAMPION', 'CHAMPION_RENTAL', 'SUMMONERICON'
################################################

# Find skin shards for champions with no owned skins
def find_shards_for_champs_with_no_skins(champions, skins, loot):
    no_skin_champs = champions_with_no_skins(champions, skins)
    champ_id_dict = champ_id_dict_maker(champions)
    shards_for_no_skin_champs = {}
    
    for champ_id in no_skin_champs:
        # First, look up all the skin ids for the champion
        skin_ids = [skin['id'] for skin in skins if skin['championId'] == champ_id]
        # Then find shards who's "storeItemId" is the same as the skin id
        shards = []
        for skin_id in skin_ids:
            for item in loot:
                if item['storeItemId'] == skin_id:
                    shards.append(item)
        if shards:
            shards_for_no_skin_champs[champ_id_dict[champ_id]] = shards
    
    return shards_for_no_skin_champs

# Takes in a dictionary of some loot data and returns a trimmed down version
def useful_champ_dict(loot_data, useful_keys):
    useful_loot = []
    for item in loot_data:
        useful_item = {key: item[key] for key in useful_keys if key in item}
        useful_loot.append(useful_item)
    return useful_loot

if __name__ == '__main__':
    champions = load_champions()
    skins = load_skins()
    loot = load_loot()

    # Print out how many owned champions and skins you have
    owned_champions = analyze_champions(champions)
    owned_skins = analyze_skins(skins)

    # Print out how many unowned champions and skins you have
    unowned_champions_list = unowned_champions(champions)
    unowned_skins_list = unowned_skins(skins)
    print(f"Unowned Champions: {len(unowned_champions_list)}")
    print(f"Unowned Skins: {len(unowned_skins_list)}")

    loot_skin_shards = get_loot_skin_shards(loot)
    shards_for_no_skin_champs = find_shards_for_champs_with_no_skins(champions, skins, loot_skin_shards)

    # Print out a detailed list of skin shards for each champion with no skins
    for champ, shards in shards_for_no_skin_champs.items():
        print(f"{champ}:")
        for shard in shards:
            print(f"  - {shard['itemDesc']} (Count: {shard['count']}) - Upgrade Cost: {shard['upgradeEssenceValue']}")

    dict_data = useful_champ_dict(loot_skin_shards, ['itemDesc', 'parentStoreItemId', 'count', 'upgradeEssenceValue', 'displayCategories', 'parentItemStatus'])

    # Also add a key at the start for the champion name
    for item in dict_data:
        item['championName'] = champ_id_dict_maker(champions).get(item['parentStoreItemId'], 'Unknown Champion')

    # Now move the 'championName' key to the front of each dictionary
    dict_data = [{**{'championName': item.pop('championName')}, **item} for item in dict_data]
    
    dict_to_csv(dict_data, 'skin_shards.csv')
    print("Analysis complete.")