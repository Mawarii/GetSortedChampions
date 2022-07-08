from riotwatcher import LolWatcher
import json


def get_current_champion_list():
    lol_watcher = LolWatcher('API-KEY')

    my_region = 'euw1'

    versions = lol_watcher.data_dragon.versions_for_region(my_region)
    champions_version = versions['n']['champion']
    current_champ_list = lol_watcher.data_dragon.champions(champions_version)
    
    return current_champ_list

def get_champ_id_name_dict():
    current_champ_list = get_current_champion_list()
    champ_ids_names = dict()
    for champ in current_champ_list['data']:
        champ_ids_names[current_champ_list['data'][champ]['key']] = champ
        
    return champ_ids_names
        
def get_champion_playrate():
    j = open("championrates.json")
    champion_playrate = json.load(j)

    return champion_playrate

def sort_champs_to_roles():
    champ_ids_names = get_champ_id_name_dict()
    champion_playrate = get_champion_playrate()
    
    LANES = ['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY']

    sorted_champions = dict()
    for lane in LANES:
        temp = list()
        for id in champ_ids_names:
            if champion_playrate['data'][str(id)][lane]['playRate'] > 0:
                temp.append(champ_ids_names[id])
        sorted_champions[lane] = temp

    with open("champs_to_roles.json", "w") as f:
        json.dump({"data":sorted_champions}, f)
        
def sort_roles_to_champs():
    champ_ids_names = get_champ_id_name_dict()
    champion_playrate = get_champion_playrate()
    
    LANES = ['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY']

    sorted_champions = dict()
    for id in champ_ids_names:
        temp = list()
        for lane in LANES:
            if champion_playrate['data'][str(id)][lane]['playRate'] > 0:
                temp.append(lane)
        sorted_champions[champ_ids_names[id]] = temp

    with open("roles_to_champs.json", "w") as f:
        json.dump({"data":sorted_champions}, f)

if __name__ == '__main__':
    sort_champs_to_roles()
    sort_roles_to_champs()
