# Special: "King's Elekk", "Sea Reaver", "Flame Leviathan", "Holy Wrath", "Chromaggus", "Tinkertown Technician", "Thistle Tea", "Cutpurse",
#   "Infest", "Headcrack", "Gnomish Experimenter", "Captain's Parrot", "Mech-Bear-Cat", "Blood Warriors", "Lock and Load", "Gazlowe",
#   "Shadowfiend", "Wilfred Fizzlebang", "Anub'ar Ambusher", "Vanish", "Kidnapper", "Echo of Mediv", "Trade Prince Gallywix", "Lorewalker Cho"
# Dragons: "Blackwing Corruptor", "Blackwing Technician", "Twilight Whelp", "Alextrasza's Champion", "Wyrmrest Agent",
#   "Twilight Guardian", "Rend Blackhand", "Chillmaw"
# Inspire: "Recruiter", "Nexus-Champion Saraad", "Colliseum Manager"
# Deathrattle: "Infest", "Explorer's Hat", "Voidcaller", "The Skeleton Knight"
# Discard: "Succubus", "Soulfire", "Darkshire Librarian", "Doomguard", "Astral Communion", "Dark Bargain", "Deathwing"

# Within this file, I've separated out names of cards in "double quotes", so that I can search for them via splitter.py.
# It also means there won't be any \'s in card names.
import Hand, Utilities

# When a card hits the board, and we can see what it's name is
def play2(entity):
    if entity['player'] == Utilities.them:
        if entity['name'] in ["Crackle", "Fireguard Destroyer", "Lightning Bolt", "Stormcrack", "Stormforged Axe", "Totem Golem", "Dunemaul Shaman", "Siltfin Spiritwalker"]:
            Utilities.overload += 1
        elif entity['name'] in ["Ancestral Knowledge", "Dust Devil", "Flamewreathed Faceless", "Forked Lightning", "Feral Spirit", "Lava Burst", "Lightning Storm", "Doomhammer"]:
            Utilities.overload += 2
        elif entity['name'] in ["Earth Elemental", "Neptulon"]:
            Utilities.overload += 3
        elif entity['name'] in ["Elemental Destruction"]:
            Utilities.overload += 5
        elif entity['name'] in ["Lava Shock", "Eternal Sentinel"]:
            Utilities.overload = 0

        elif entity['name'] == "Varian Wrynn":
            Legendaries.varianWrynn = True

        elif entity['name'] == "A Light in the Darkness":
            Hand.draw(entity, note='A random minion with +1/+1')
        elif entity['name'] == "Dark Peddler":
            Hand.draw(entity, note='A 1-cost card')
        elif entity['name'] == "Ethereal Conjurer":
            Hand.draw(entity, note='A spell')
        elif entity['name'] == "Gorillabot A-3":
            Hand.draw(entity, note='A mech')
        elif entity['name'] == "Jeweled Scarab":
            Hand.draw(entity, note='A 3-cost card')
        elif entity['name'] == "Museum Curator":
            Hand.draw(entity, note='A deathrattle card')
        elif entity['name'] == "Raven Idol":
            Hand.draw(entity, note='A minion or a spell')
        elif entity['name'] == "Tomb Spider":
            Hand.draw(entity, note='A beast')
        elif entity['name'] == "Journey Below":
            Hand.draw(entity, note='A deathrattle card')
        elif entity['name'] == "Arch-Thief Rafaam":
            Hand.draw(entity, note='A powerful artifact')

        elif entity['name'] == "Burgle":
            Hand.draw(entity, note='A random card from your class')
            Hand.draw(entity, note='A random card from your class')
        elif entity['name'] == "Cabalist's Tomb":
            Hand.draw(entity, note='A random Mage spell')
            Hand.draw(entity, note='A random Mage spell')
            Hand.draw(entity, note='A random Mage spell')
        elif entity['name'] == "Call Pet":
            Hand.draw(entity, note='If it\'s a beast, cost -4')
        elif entity['name'] == "Far Sight":
            Hand.notes.append('Costs (3) less')
        elif entity['name'] == "Grand Crusader":
            Hand.draw(entity, note='A random Paladin card')
        elif entity['name'] == "Mind Vision":
            Hand.draw(entity, note='A card from your hand')
        elif entity['name'] == "Mukla, Tyrant of the Vale":
            Hand.draw(entity, note='A Banana')
            Hand.draw(entity, note='A Banana')
        elif entity['name'] == "Neptulon":
            Hand.draw(entity, note='A random Murloc')
            Hand.draw(entity, note='A random Murloc')
            Hand.draw(entity, note='A random Murloc')
            Hand.draw(entity, note='A random Murloc')
        elif entity['name'] == "Nefarian":
            Hand.draw(entity, note='A random card from your class')
            Hand.draw(entity, note='A random card from your class')
        elif entity['name'] == "Sense Demons":
            Hand.draw(entity, note='A demon')
            Hand.draw(entity, note='A demon')
        elif entity['name'] == "Thoughtsteal":
            Hand.draw(entity, note='A card from your deck')
            Hand.draw(entity, note='A card from your deck')
        elif entity['name'] == "Toshley":
            Hand.draw(entity, note='Spare Part')
        elif entity['name'] == "Unstable Portal":
            Hand.draw(entity, note='Random minion', cost=-3)
        elif entity['name'] == "Wild Growth":
            if Utilities.resources == '10':
                Hand.draw(entity, note='Excess Mana')
        elif entity['name'] == "Xaril, Poisoned Mind":
            Hand.draw(entity, note='A random toxin')
    elif entity['player'] == Utilities.us:
        if entity['name'] == "King Mukla":
            Hand.draw(entity, note='A Banana')
            Hand.draw(entity, note='A Banana')
        elif entity['name'] == "Mulch":
            Hand.draw(entity, note='A random minion')
    # if entity['player'] in [Utilities.us, Utilities.them]:
    if entity['name'] == "Spellslinger":
        Hand.draw(entity, note='A random spell')
    elif entity['name'] == "Elite Tauren Chieftain":
        Hand.draw(entity, note='A Power Chord card')

# When a card hits the board and we can see what its name and its target's name is.
def play3(entity, target):
    if entity['player'] == Utilities.them:
        if entity['name'] in ["Ancient Brewmaster", "Convert", "Time Rewinder", "Youthful Brewmaster"]:
            Hand.draw(target, note=target['name'])
        elif entity['name'] in ["Bloodthistle Toxin", "Shadowstep"]:
            Hand.draw(target, note=target['name'], cost=-2)
        elif entity['name'] == "Convert":
            Hand.draw(target, note=target['name'])
        elif entity['name'] == "Shadowcaster":
            Hand.draw(target, note='A 1/1 copy of %s which costs (1)' % target['name'])
    elif entity['player'] == Utilities.us:
        if entity['name'] == "Freezing Trap":
            Hand.draw(target, note=target['name'], cost=+2)
        elif entity['name'] == "Sap":
            Hand.draw(target, note=target['name'])
    if entity['name'] == "Dream" and target['player'] == Utilities.them:
        Hand.draw(target, note=target['name'])

def die(entity):
    if entity['player'] == Utilities.them:
        if entity['name'] == "Anub'arak":
            Hand.draw(entity, note='Anub\'arak')
        elif entity['name'] == "Clockwork Gnome":
            Hand.draw(entity, note='Spare Part')
        elif entity['name'] == "Rhonin":
            Hand.draw(entity, note='Arcane Missles')
            Hand.draw(entity, note='Arcane Missles')
            Hand.draw(entity, note='Arcane Missles')
        elif entity['name'] == "Shifting Shade":
            Hand.draw(entity, note='A card from your deck')
        elif entity['name'] == "Tentacles for Arms":
            Hand.draw(entity, note='Tentacles for Arms')
        elif entity['name'] == "Tomb Pillager":
            Hand.draw(entity, note='The Coin')
        elif entity['name'] == "Toshley":
            Hand.draw(entity, note='Spare Part')
        elif entity['name'] == "Undercity Huckster":
            Hand.draw(entity, note='A card from your class')
        elif entity['name'] == "Xaril, Poisoned Mind":
            Hand.draw(entity, note='A random toxin')
        elif entity['name'] == "Webspinner":
            Hand.draw(entity, note='A random beast')
    # if entity['player'] in [Utilities.us, Utilities.them]:
    if entity['name'] == "Mechanical Yeti":
        Hand.draw(entity, note='Spare Part')

# Be careful of Blessing of Wisdom (others?) which can 'trigger' an effect on a card that already has a triggered effect.
# This isn't very well encapsulated, but it's also the extreme edge-case cards that are hard to deal with otherwise.
def trigger(entity):
    if entity['player'] == Utilities.them:
        if entity['name'] == "Alarm-o-Bot":
            Hand.draw(entity, note="Alarm-o-Bot")
        elif entity['name'] == "Archmage Antonidas":
            Hand.draw(entity, note='Fireball')
        elif entity['name'] == "Emperor Thaurissan":
            for card in Hand.hand:
                card.cost -= 1
        elif entity['name'] == "Ysera":
            Hand.draw(entity, note='A Dream card')

def turnover():
    if Utilities.overload != 0:
        print 'Overload next turn:', Utilities.overload
        Utilities.overload = 0
