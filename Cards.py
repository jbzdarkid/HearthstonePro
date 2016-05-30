# Special: King's Elekk, Sea Reaver, Flame Leviathan, Holy Wrath, Archmage Antonidas, Chromaggus, Tinkertown Technician, Thistle Tea, Cutpurse, Infest, Headcrack, Varian Wrynn, Gnomish Experimenter, Far Sight, Captain's Parrot, Mech-Bear-Cat, Blood Warriors, Lock and Load, Gazlowe
# Dragons: Blackwing Corruptor, Blackwing Technician, Twilight Whelp, Alextrasza's Champion, Wyrmrest Agent, Twilight Guardian, Rend Blackhand, Chillmaw
# Inspire: Recruiter, Nexus-Champion Saraad
# Targetted: Bloodthistle Toxin, Dream, Time Rewinder, Sap, Ancient Brewmaster, Anub'ar Ambusher, Freezing Trap, Shadowstep, Vanish*, Youthful Brewmaster, Alarm-o-Bot, Coliseum Manager, Kidnapper, Anub'arak, The Skeleton Knight, Shadowcaster, Echo of Mediv, Convert, Trade Prince Gallywix, Lorewalker Cho
# Deathrattle: Infest*, Explorer's Hat, Voidcaller, The Skeleton Knight

import Hand

def reset():
    global overload, resources
    overload = 0
    resources = None

reset()

# When a card hits the board, and we can see what it's name is
def play2(entity):
    global overload
    if entity['player'] == Hand.them:
        if entity['name'] in ['Crackle', 'Fireguard Destroyer', 'Lightning Bolt', 'Stormcrack', 'Stormforged Axe', 'Totem Golem', 'Dunemaul Shaman', 'Siltfin Spiritwalker']:
            overload += 1
        elif entity['name'] in ['Ancestral Knowledge', 'Dust Devil', 'Flamewreathed Faceless', 'Forked Lightning', 'Feral Spirit', 'Lava Burst', 'Lightning Storm', 'Doomhammer']:
            overload += 2
        elif entity['name'] in ['Earth Elemental', 'Neptulon']:
            overload += 3
        elif entity['name'] in ['Elemental Destruction']:
            overload += 5
        elif entity['name'] in ['Lava Shock', 'Eternal Sentinel']:
            overload = 0

        elif entity['name'] == 'Burgle':
            Hand.draw(entity, note='A random card from your class')
            Hand.draw(entity, note='A random card from your class')
        elif entity['name'] == 'Cabalist\'s Tomb':
            Hand.draw(entity, note='A random Mage spell')
            Hand.draw(entity, note='A random Mage spell')
            Hand.draw(entity, note='A random Mage spell')
        elif entity['name'] == 'Call Pet':
            Hand.draw(entity, note='If it\'s a beast, cost -4')
        elif entity['name'] == 'Grand Crusader':
            Hand.draw(entity, note='A random Paladin card')
        elif entity['name'] == 'Mind Vision':
            Hand.draw(entity, note='A card from your hand')
        elif entity['name'] == 'Mukla, Tyrant of the Vale':
            Hand.draw(entity, note='A Banana')
            Hand.draw(entity, note='A Banana')
        elif entity['name'] == 'Neptulon':
            Hand.draw(entity, note='A random Murloc')
            Hand.draw(entity, note='A random Murloc')
            Hand.draw(entity, note='A random Murloc')
            Hand.draw(entity, note='A random Murloc')
        elif entity['name'] == 'Nefarian':
            Hand.draw(entity, note='A random card from your class')
            Hand.draw(entity, note='A random card from your class')
        elif entity['name'] == 'Sense Demons':
            Hand.draw(entity, note='A demon')
            Hand.draw(entity, note='A demon')
        elif entity['name'] == 'Thoughtsteal':
            Hand.draw(entity, note='A card from your deck')
            Hand.draw(entity, note='A card from your deck')
        elif entity['name'] == 'Toshley':
            Hand.draw(entity, note='Spare Part')
        elif entity['name'] == 'Unstable Portal':
            Hand.draw(entity, note='Random minion', cost=-3)
        elif entity['name'] == 'Wild Growth':
            if resources == '10':
                Hand.draw(entity, note='Excess Mana')
        elif entity['name'] == 'Xaril, Poisoned Mind':
            Hand.draw(entity, note='A random toxin')
    elif entity['player'] == Hand.us:
        if entity['name'] == 'King Mukla':
            Hand.draw(entity, note='A Banana')
            Hand.draw(entity, note='A Banana')
        elif entity['name'] == 'Mulch':
            Hand.draw(entity, note='A random minion')
    # if entity['player'] in [Hand.us, Hand.them]:
    if entity['name'] == 'Spellslinger':
        Hand.draw(entity, note='A random spell')
    elif entity['name'] == 'Elite Tauren Chieftain':
        Hand.draw(entity, note='A Power Chord card')

def die(entity):
    if entity['player'] == Hand.them:
        if entity['name'] == 'Anub\'arak':
            Hand.draw(entity, note='Anub\'arak')
        elif entity['name']    == 'Clockwork Gnome':
            Hand.draw(entity, note='Spare Part')
        elif entity['name'] == 'Rhonin':
            Hand.draw(entity, note='Arcane Missles')
            Hand.draw(entity, note='Arcane Missles')
            Hand.draw(entity, note='Arcane Missles')
        elif entity['name'] == 'Shifting Shade':
            Hand.draw(entity, note='A card from your deck')
        elif entity['name'] == 'Tentacles for Arms':
            Hand.draw(entity, note='Tentacles for Arms')
        elif entity['name'] == 'Tomb Pillager':
            Hand.draw(entity, note='The Coin')
        elif entity['name'] == 'Toshley':
            Hand.draw(entity, note='Spare Part')
            Hand.draw(entity)
        elif entity['name'] == 'Undercity Huckster':
            Hand.draw(entity, note='A card from your class')
        elif entity['name'] == 'Xaril, Poisoned Mind':
            Hand.draw(entity, note='A random toxin')
        elif entity['name'] == 'Webspinner':
            Hand.draw(entity, note='A random beast')
    # if entity['player'] in [Hand.us, Hand.them]:
    if entity['name'] == 'Mechanical Yeti':
        Hand.draw(entity, note='Spare Part')

def discover(source):
    if source['player'] == Hand.them:
        if 'name' not in source: # Sir Finley Mrrgglton
            return
        elif source['name'] == 'A Light in the Darkness':
            Hand.draw(source, note='A random minion with +1/+1')
        elif source['name'] == 'Dark Peddler':
            Hand.draw(source, note='A 1-cost card')
        elif source['name'] == 'Ethereal Conjurer':
            Hand.draw(source, note='A spell')
        elif source['name'] == 'Gorillabot A-3':
            Hand.draw(source, note='A mech')
        elif source['name'] == 'Jeweled Scarab':
            print '165'
            Hand.draw(source, note='A 3-cost card')
        elif source['name'] == 'Museum Curator':
            Hand.draw(source, note='A deathrattle card')
        elif source['name'] == 'Raven Idol':
            Hand.draw(source, note='A minion or a spell')
        elif source['name'] == 'Tomb Spider':
            Hand.draw(source, note='A beast')
        elif source['name'] == 'Journey Below':
            Hand.draw(source, note='A deathrattle card')
        elif source['name'] == 'Arch-Thief Rafaam':
            Hand.draw(source, note='A powerful artifact')

# This isn't very well encapsulated, but it's also the extreme edge-case cards that are hard to deal with otherwise.
def trigger(entity):
    if entity['player'] == Hand.them:
        if entity['name'] == 'Emperor Thaurissan':
            for card in Hand.hand:
                card.cost -= 1
        elif entity['name'] == 'Ysera':
            Hand.draw(source, note='A Dream card')

def turnover(turn):
    global overload
    offset = 1 if Hand.wentFirst else 0
    if turn%2 == offset:
        if overload != 0:
            print 'Overload next turn:', overload
            overload = 0
