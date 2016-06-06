# http://hearthstone.gamepedia.com/Enchantment_list#Regular_play

# Todo: "Chillmaw"

import Hand, Utilities

def reset():
    global sets
    sets = []

reset()

def play2(entity):
    if entity['player'] == Utilities.them:
        removeEntity(card.id)
        if entity['name'] in ["Blackwing Corruptor", "Rend Blackhand"]:
            noDragon()

def play3(entity):
    if entity['player'] == Utilities.them:
        removeEntity(card.id)
        if entity['name'] == ["Blackwing Corruptor", "Rend Blackhand"]:
            hasDragon()

# When a triggered ability enters play, usually attatched to another creature.
def play4(entity):
    if entity['player'] == Utilities.them:
        # "Alextrasza's Champion", "Wyrmrest Agent", "Blackwing Technician", "Twilight Guardian", "Twilight Whelp"
        if entity['name'] in ["Alexstrasza's Boon", "Bring it on!", "Dragon Blood", "Twilight's Embrace", "Twilight Endurance"]:
            hasDragon()
        elif entity['name']

def die(entity):
    pass

def removeEntity(id):
    for i in range(len(sets)):
        for j in range(len(sets[i])):
            if sets[i][j].id == id:
                del sets[i][j]
                if sets[i] == []:
                    del sets[i]
                return True
    return False

def hasDragon():
    sets.append([card.id for card in Hand.hand])

def noDragon():
    for card in hand:
        removeEntity(card.id)

def turnover():
    pass