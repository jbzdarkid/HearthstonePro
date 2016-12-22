import logging
import Hand, Utilities

# There's a few things to do about dragons.
# 1. When a card is played that has a triggered effect, >= 1 card in hand must be a dragon.
# 1a. If (at some later date) a card is played from that set which is a dragon, no information is known about the remaining cards.
# 1b. If (at some later date) all cards but one are played from that set and are not dragons, then the remaining card is a dragon.
# 1c. Info from 1b. may be relevant with 2 cards remaining.
# 2. When a card is played that fails to have a triggered effect, 0 cards in hand are dragons.
# 2a. If (at some later date) a card is played which does have a triggered effect, these cards are excluded from the set.
# 3. If a card which is not a dragon is returned to hand, we know that it still isn't a dragon.

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
    global noDragonBlock
    if noDragonBlock: # Block should have had a dragon effect
        noDragon()
        noDragonBlock = False

# When a card is played and we can see its position in the hand
def play(entity):
    global cardId
    if entity['player'] == Utilities.them:
        cardId = id(Hand.hand[int(entity['zonePos'])-1])

# When a card is played and we can see its name, and it has no targets
def play2(entity):
    global noDragonBlock
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
        if entity['name'] == ["Blackwing Corruptor", "Book Wyrm", "Rend Blackhand"]:
            hasDragon()

# When a triggered ability enters play, usually attatched to another creature.
def setaside(entity):
    global noDragonBlock
    if entity['player'] == Utilities.them:
        if noDragonBlock:
            noDragonBlock = False
            hasDragon()

def die(entity):
    global noDragonBlock
    if entity['player'] == Utilities.them:
        # Need the name of the death trigger
        if entity['name'] == "Chillmaw":
            noDragonBlock = True
        elif entity['name'] == "Deathwing, Dragonlord":
            pass

# The hand has a dragon, so we create a new set of cards, one of which must be a dragon
def hasDragon():
    logging.info('Opponent has a dragon in their hand')
    global sets
    sets.append([id(card) for card in Hand.hand])

# The hand has no dragons, so we wipe all information about sets.
def noDragon():
    global sets
    logging.info('Opponent does not have a dragon in their hand')
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
    for set in sets:
        # if len(set) > 2:
            # continue
        card_ids = []
        for i, card in enumerate(Hand.hand):
            if id(card) in set:
                card_ids.append(str(i+1))
        print 'One of cards #' + ', '.join(card_ids)  + ' is a dragon'
