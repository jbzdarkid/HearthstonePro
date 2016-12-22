import Hand, Utilities

# So, each card needs a dragonSets and a notDragon field.
# When a card is played and it fails to have a triggered effect, all cards in the hand set notDragon=True and dragonSets=[].
# When a card is played and has a triggered effect, all cards in the hand with notDragon=False have dragonSets.append(newSet)
# When a card is played and it's a dragon, for each set it's a part of, all cards in hand have dragonSets.remove(set). If the sets becomes empty, this DOES NOT mean the card isn't a dragon.
# Each printout, any sets with 2 or 1 members should be mentioned.

DRAGONS = [
    'Alextrasza', 'Azure Drake',
    'Black Whelp', 'Book Wyrm',
    'Chillmaw', 'Chromaggus', 'Coldarra Drake',
    'Deathwing', 'Deathwing, Dragonlord', 'Dragon Consort', 'Dragonkin Sorceror', 'Drakanoid Crusher', 'Drakanoid Operative',
    'Emerald Drake',
    'Faerie Dragon',
    'Hungry Dragon',
    'Malygos',
    'Midnight Drake',
    'Nefarian', 'Nozdormu',
    'Onyxia',
    'Scaled Nightmare',
    'Twilight Drake', 'Twilight Guardian', 'Twilight Whelp',
    'Volcanic Drake',
    'Whelp',
    'Ysera',
]

def reset():
    global sets, noDragonBlock, cardId
    sets = []
    noDragonBlock = False

reset()

# End of a block
def blockEnd(): 
    if noDragonBlock: # Block should have had a dragon effect
        noDragon()
        noDragonBlock = False

# When a card is played and we can see its position in the hand
def play(entity):
    global cardId
    cardId = id(hand[int(entity['zonePos'])-1])

# When a card is played and we can see its name, and it has no targets
def play2(entity):
    if entity['player'] == Utilities.them:
        if entity['name'] in DRAGONS:
            isDragon(cardId)
        else:
            isNotDragon(cardId)
        if entity['name'] in ["Blackwing Corruptor", "Rend Blackhand"]:
            noDragon()
        elif entity['name'] in ["Alextrasza's Champion", "Wyrmrest Agent", "Blackwing Technician", "Twilight Guardian", "Twilight Whelp"]:
            noDragonBlock = True

def play3(entity, target):
    if entity['player'] == Utilities.them:
        if entity['name'] in DRAGONS:
            isDragon(cardId)
        else:
            isNotDragon(cardId)
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
        if entity['name'] == "Chillmaw": # Need the name of the death trigger
            noDragonBlock = True

# The hand has a dragon, so we create a new set of cards, one of which must be a dragon
def hasDragon():
    global sets
    sets.append([id(card) for card in Hand.hand])

# The hand has no dragons, so we wipe all information about sets.
def noDragon():
    global sets
    sets = []

# A card is revealed to be a dragon, so we wipe all sets it was a part of
def isDragon(id):
    global sets
    sets = [set for set in sets if id not in set]
    
# A card is revealed not to be a dragon, so we remove it from all sets
def isNotDragon(id):
    global sets
    for set in sets:
        try:
            set.remove(id)
        except ValueError:
            pass

def turnover():
    print 'Dragons.py<104>', sets
