import Hand, Utilities

# If a card is played and it *is* a dragon, remove any set it's a part of (no information )

def reset():
    global sets, noDragonBlock
    sets = []
    noDragonBlock = False

reset()

def blockEnd():
    if noDragonBlock:
        noDragon()
        noDragonBlock = False

def play2(entity):
    if entity['player'] == Utilities.them:
        removeEntity(entity['id'])
        if entity['name'] in ["Blackwing Corruptor", "Rend Blackhand"]:
            noDragon()
        elif entity['name'] in ["Alextrasza's Champion", "Wyrmrest Agent", "Blackwing Technician", "Twilight Guardian", "Twilight Whelp"]:
            noDragonBlock = True

def play3(entity, target):
    if entity['player'] == Utilities.them:
        removeEntity(entity['id'])
        if entity['name'] == ["Blackwing Corruptor", "Rend Blackhand"]:
            hasDragon()

# When a triggered ability enters play, usually attatched to another creature.
def play4(entity):
    if entity['player'] == Utilities.them:
        if entity['name'] in ["Alexstrasza's Boon", "Bring it on!", "Dragon Blood", "Twilight's Embrace", "Twilight Endurance"]:
            noDragonBlock = False
            hasDragon()

def die(entity):
    if entity['player'] == Utilities.them:
        if entity['name'] == "Chillmaw": # Needs to be able to fail
            noDragonBlock = True

def removeEntity(id):
    for i in range(len(sets)):
        for j in range(len(sets[i])):
            if sets[i][j] == id:
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
    for set in sets:
        if len(set) < 2:
            pass
