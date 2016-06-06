# http://hearthstone.gamepedia.com/Enchantment_list#Regular_play

import Hand, Utilities

# When a triggered ability enters play, usually attatched to another creature.
def play4(entity):
    if entity['player'] == Utilities.them:
        if entity['name'] == "Dragon Blood": # "Blackwing Technician"
            pass
