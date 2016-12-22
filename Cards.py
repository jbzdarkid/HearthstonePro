'''
Special:
"Anub'ar Ambusher"
"Blood Warriors"
"Burgly Bully"
"Captain's Parrot"
"Chromaggus"
"Echo of Mediv"
"Ethereal Peddler"
"Flame Leviathan"
"Getaway Kodo"
"Gnomish Experimenter"
"Headcrack"
"Holy Wrath"
"Ivory Knight"
"Kazakus"
"King's Elekk"
"Krul the Unshackled"
"Lock and Load"
"Lorewalker Cho"
"Sea Reaver"
"Shadowfiend"
"Shaku, the Collector"
"Small-Time Recruits"
"Thistle Tea"
"Tinkertown Technician"
"Trade Prince Gallywix"
"Vanish"
"Wilfred Fizzlebang"
"Wrathion"
'''
# Inspire: "Recruiter", "Nexus-Champion Saraad", "Colliseum Manager"
# Deathrattle: "Infest", "Explorer's Hat", "Voidcaller", "The Skeleton Knight"
# Discard: "Succubus", "Soulfire", "Darkshire Librarian", "Doomguard", "Astral Communion", "Dark Bargain", "Deathwing"
# Buff: "Smuggler's Crate", "Hidden Cache", "Trogg Beastrager", "Grimscale Chum", "Grimestreet Outfitter", "Grimestreet Enforcer", "Grimestreet Gadgeteer", "Stolen Goods", "Grimestreet Pawnbroker", "Brass Knuckles", "Hobart Grapplehammer", "Grimestreet Smuggler", "Don Han'Cho"


# Within this file, I've separated out names of cards in "double quotes", so that I can search for them via splitter.py.
# It also means there won't be any \'s in card names.
import logging
import Hand, Utilities, Legendaries

# When a card hits the board, and we can see what its name is
def play2(entity):
    if entity['player'] == Utilities.them:
        logging.info('Opponent plays %s' % entity['name'])
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
            Hand.draw(source='random', kind='minion', buff=+1)
        elif entity['name'] == "Arch-Thief Rafaam":
            Hand.draw(note='A powerful artifact', kind='spell')
        elif entity['name'] == "Babbling Book":
            Hand.draw(source='random', hero='mage', kind='spell')
        elif entity['name'] == "Burgle":
            Hand.draw(source='random', hero='[your class]') # FIXME
            Hand.draw(source='random', hero='[your class]') # FIXME
        elif entity['name'] == "Cabalist's Tomb":
            Hand.draw(source='random', hero='mage', kind='spell')
            Hand.draw(source='random', hero='mage', kind='spell')
            Hand.draw(source='random', hero='mage', kind='spell')
        elif entity['name'] == "Dark Peddler":
            Hand.draw(note='A 1-cost card')
        elif entity['name'] == "Ethereal Conjurer":
            Hand.draw(source='discovered', hero='mage', kind='spell')
        elif entity['name'] == "Finders Keepers":
            Hand.draw(hero='shaman', note='A card with overload')
        elif entity['name'] == "Gorillabot A-3":
            Hand.draw(kind='mech minion')
        elif entity['name'] == "Grand Crusader":
            Hand.draw(source='random', hero='paladin')
        elif entity['name'] == "Grimestreet Informant":
            Hand.draw(hero='hunter, paladin, or warrior')
        elif entity['name'] == "I Know a Guy":
            Hand.draw(kind='taunt minion')
        elif entity['name'] == "Jeweled Scarab":
            Hand.draw(note='A 3-cost card')
        elif entity['name'] == "Journey Below":
            Hand.draw(note='A deathrattle card')
        elif entity['name'] == "Kabal Chemist":
            Hand.draw(kind='potion spell')
        elif entity['name'] == "Lotus Agents":
            Hand.draw(hero='druid, rogue, or shaman')
        elif entity['name'] == "Mind Vision":
            Hand.draw(note='A card from your hand')
        elif entity['name'] == "Mukla, Tyrant of the Vale":
            Hand.draw(note='Banana', kind='spell')
            Hand.draw(note='Banana', kind='spell')
        elif entity['name'] == "Museum Curator":
            # I'm ignoring "Tentacles For Arms" because it's bad
            Hand.draw(note='A deathrattle card', kind='minion')
        elif entity['name'] == "Nefarian":
            Hand.draw(source='random', hero='[your class]') # FIXME
            Hand.draw(source='random', hero='[your class]') # FIXME
        elif entity['name'] == "Neptulon":
            Hand.draw(source='random', kind='murloc minion')
            Hand.draw(source='random', kind='murloc minion')
            Hand.draw(source='random', kind='murloc minion')
            Hand.draw(source='random', kind='murloc minion')
        elif entity['name'] == "Raven Idol":
            Hand.draw(kind='minion or spell')
        elif entity['name'] == "Sense Demons":
            Hand.draw(kind='demon minion')
            Hand.draw(kind='demon minion')
        elif entity['name'] == "Swashburglar":
            Hand.draw(source='random', hero='[your class]') # FIXME
        elif entity['name'] == "Thoughtsteal":
            Hand.draw(note='A random card from your deck')
            Hand.draw(note='A random card from your deck')
        elif entity['name'] == "Tomb Spider":
            Hand.draw(kind='beast minion')
        elif entity['name'] == "Toshley":
            Hand.draw(note='Spare Part', kind='spell')
        elif entity['name'] == "Unstable Portal":
            Hand.draw(source='random', kind='minion', cost=-3)
        elif entity['name'] == "Wild Growth":
            if Utilities.resources == '10':
                Hand.draw(note='Excess Mana', hero='druid', kind='spell')
        elif entity['name'] == "Xaril, Poisoned Mind":
            Hand.draw(source='random', kind='toxin spell')

        elif entity['name'] == "Call Pet":
            Hand.notes.append('If it\'s a beast, cost -4')
        elif entity['name'] == "Far Sight":
            Hand.notes.append('Costs (3) less')
    elif entity['player'] == Utilities.us:
        if entity['name'] == "King Mukla":
            Hand.draw(kind='Banana')
            Hand.draw(kind='Banana')
        elif entity['name'] == "Mulch":
            Hand.draw(source='random', kind='minion')
    # if entity['player'] in [Utilities.us, Utilities.them]:
    if entity['name'] == "Elite Tauren Chieftain":
        Hand.draw(kind='Power Chord spell')
    elif entity['name'] == "Spellslinger":
        Hand.draw(source='random', kind='spell')

# When a card hits the board and we can see what its name and its target's name is.
def play3(entity, target):
    if entity['player'] == Utilities.them:
        logging.info('Opponent plays %s targetting %s' % (entity['name'], target['name']))
        if entity['name'] in ["Ancient Brewmaster", "Convert", "Gadgetzan Ferryman", "Time Rewinder", "Youthful Brewmaster"]:
            Hand.draw(note=target['name'], kind='minion')
        elif entity['name'] in ["Bloodthistle Toxin", "Shadowstep"]:
            Hand.draw(note=target['name'], kind='minion', cost=-2)
        elif entity['name'] == "Convert":
            Hand.draw(note=target['name'], kind='minion')
        elif entity['name'] == "Shadowcaster":
            Hand.draw(note='A 1/1 copy of %s which costs (1)' % target['name'], kind='minion')
    elif entity['player'] == Utilities.us:
        if entity['name'] == "Freezing Trap":
            Hand.draw(note=target['name'], kind='minion', cost=+2)
        elif entity['name'] == "Sap":
            Hand.draw(note=target['name'], kind='minion')
    if target['player'] == Utilities.them:
        if entity['name'] in ["Dream", "Kindapper"]:
            Hand.draw(note=target['name'], kind='minion')

def die(entity):
    if entity['player'] == Utilities.them:
        logging.info('Opponent\'s %s dies' % entity['name'])
        if entity['name'] == "Anub'arak":
            Hand.draw(note='Anub\'arak')
        elif entity['name'] == "Clockwork Gnome":
            Hand.draw(note='Spare Part', kind='spell')
        elif entity['name'] == "Deadly Fork":
            Hand.draw(note='Sharp Fork', kind='weapon')
        elif entity['name'] == "Nerubian Spores": # "Infest"
            Hand.draw()
        elif entity['name'] == "Rhonin":
            Hand.draw(note='Arcane Missles', hero='mage', kind='spell')
            Hand.draw(note='Arcane Missles', hero='mage', kind='spell')
            Hand.draw(note='Arcane Missles', hero='mage', kind='spell')
        elif entity['name'] == "Shifting Shade":
            Hand.draw(note='A card from your deck')
        elif entity['name'] == "Tentacles for Arms":
            Hand.draw(note='Tentacles for Arms')
        elif entity['name'] == "Tomb Pillager":
            Hand.draw(note='The Coin', kind='spell')
        elif entity['name'] == "Toshley":
            Hand.draw(note='Spare Part', kind='spell')
        elif entity['name'] == "Undercity Huckster":
            Hand.draw(source='random', hero='[your class]') # FIXME
        elif entity['name'] == "Xaril, Poisoned Mind":
            Hand.draw(source='random', kind='toxin')
        elif entity['name'] == "Webspinner":
            Hand.draw(source='random', kind='beast minion')
    # if entity['player'] in [Utilities.us, Utilities.them]:
    if entity['name'] == "Mechanical Yeti":
        Hand.draw(note='Spare Part', kind='spell')

# Be careful of Blessing of Wisdom (others?) which can 'trigger' an effect on a card that already has a triggered effect.
def trigger(entity):
    if entity['player'] == Utilities.them:
        logging.info('Opponent\'s %s triggers' % entity['name'])
        if entity['name'] == "Alarm-o-Bot":
            Hand.draw(note='Alarm-o-Bot', kind='minion')
        elif entity['name'] == "Archmage Antonidas":
            Hand.draw(note='Fireball', hero='mage', kind='spell')
        elif entity['name'] == "Cutpurse":
            Hand.draw(note='The Coin', kind='spell')
        elif entity['name'] == "Emperor Thaurissan":
            for card in Hand.hand:
                card.cost -= 1
        elif entity['name'] == "Gazlowe":
            Hand.draw(source='random', kind='mech minion')
        elif entity['name'] == "Mech-Bear-Cat":
            Hand.draw(note='Spare Part', kind='spell')
        elif entity['name'] == "Kabal Trafficker":
            Hand.draw(source='random', kind='demon minion')
        elif entity['name'] == "Ysera":
            Hand.draw(note='A Dream card', kind='spell')

def turnover():
    if Utilities.overload != 0:
        print 'Overload next turn:', Utilities.overload
        Utilities.overload = 0
