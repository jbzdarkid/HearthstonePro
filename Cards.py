# Special: King's Elekk, Sea Reaver, Flame Leviathan, Holy Wrath, Archmage Antonidas, Ysera, Chromaggus, Tinkertown Technician, Thistle Tea, Cutpurse, Infest, Headcrack, Varian Wrynn, Gnomish Experimenter, Far Sight, Captain's Parrot, Mech-Bear-Cat, Blood Warriors, Lock and Load, Gazlowe
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
			Hand.notes.append('A random card from your class')
			Hand.notes.append('A random card from your class')
			Hand.draw(entity)
			Hand.draw(entity)
		elif entity['name'] == 'Cabalist\'s Tomb':
			Hand.notes.append('A random Mage spell')
			Hand.notes.append('A random Mage spell')
			Hand.notes.append('A random Mage spell')
			Hand.draw(entity)
			Hand.draw(entity)
			Hand.draw(entity)
		elif entity['name'] == 'Call Pet':
			Hand.notes.append('If it\'s a beast, cost -4')
		elif entity['name'] == 'Grand Crusader':
			Hand.notes.append('A random Paladin card')
			Hand.draw(entity)
		elif entity['name'] == 'Mind Vision':
			Hand.notes.append('A card from your hand')
			Hand.draw(entity)
		elif entity['name'] == 'Mukla, Tyrant of the Vale':
			Hand.notes.append('A Banana')
			Hand.notes.append('A Banana')
			Hand.draw(entity)
			Hand.draw(entity)
		elif entity['name'] == 'Neptulon':
			Hand.notes.append('A random Murloc')
			Hand.notes.append('A random Murloc')
			Hand.notes.append('A random Murloc')
			Hand.notes.append('A random Murloc')
			Hand.draw(entity)
			Hand.draw(entity)
			Hand.draw(entity)
			Hand.draw(entity)
		elif entity['name'] == 'Nefarian':
			Hand.notes.append('A random card from your class')
			Hand.notes.append('A random card from your class')
			Hand.draw(entity)
			Hand.draw(entity)
		elif entity['name'] == 'Sense Demons':
			Hand.notes.append('A demon')
			Hand.notes.append('A demon')
			Hand.draw(entity)
			Hand.draw(entity)
		elif entity['name'] == 'Thoughsteal':
			Hand.notes.append('A card from your deck')
			Hand.notes.append('A card from your deck')
			Hand.draw(entity)
			Hand.draw(entity)
		elif entity['name'] == 'Toshley':
		 	Hand.notes.append('Spare Part')
			Hand.draw(entity)
		elif entity['name'] == 'Unstable Portal':
		 	Hand.notes.append('Random minion')
		 	Hand.draw(entity)
		 	Hand.hand[-1].cost -= 3
		elif entity['name'] == 'Wild Growth':
			if resources == '10':
				Hand.notes.append('Excess Mana')
				Hand.draw(entity)
		elif entity['name'] == 'Xaril, Poisoned Mind':
			Hand.notes.append('A random toxin')
			Hand.draw(entity)
	elif entity['player'] == Hand.us:
		if entity['name'] == 'King Mukla':
			Hand.notes.append('A Banana')
			Hand.notes.append('A Banana')
			Hand.draw(entity)
			Hand.draw(entity)
		elif entity['name'] == 'Mulch':
			Hand.notes.append('A random minion')
			Hand.draw(entity)
	# if entity['player'] in [Hand.us, Hand.them]:
	if entity['name'] == 'Spellslinger':
		Hand.notes.append('A random spell')
		Hand.draw(entity)
	elif entity['name'] == 'Elite Tauren Chieftain':
		Hand.notes.append('A Power Chord card')
		Hand.draw(entity)

def die(entity):
	if entity['player'] == Hand.them:
		if entity['name'] == 'Anub\'arak':
			Hand.notes.append('Anub\'arak')
			Hand.draw(entity)
		elif entity['name']	== 'Clockwork Gnome':
			Hand.notes.append('Spare Part')
			Hand.draw(entity)
		elif entity['name'] == 'Rhonin':
			Hand.notes.append('Arcane Missles')
			Hand.notes.append('Arcane Missles')
			Hand.notes.append('Arcane Missles')
			Hand.draw(entity)
			Hand.draw(entity)
			Hand.draw(entity)
		elif entity['name'] == 'Shifting Shade':
			Hand.notes.append('A card from your deck')
			Hand.draw(entity)
		elif entity['name'] == 'Tentacles for Arms':
			Hand.notes.append('Tentacles for Arms')
			Hand.draw(entity)
		elif entity['name'] == 'Tomb Pillager':
			Hand.notes.append('The Coin')
			Hand.draw(entity)
		elif entity['name'] == 'Toshley':
			Hand.notes.append('Spare Part')
			Hand.draw(entity)
		elif entity['name'] == 'Undercity Huckster':
			Hand.notes.append('A card from your class')
			Hand.draw(entity)
		elif entity['name'] == 'Xaril, Poisoned Mind':
			Hand.notes.append('A random toxin')
			Hand.draw(entity)
		elif entity['name'] == 'Webspinner':
			Hand.notes.append('A random beast')
			Hand.draw(entity)
	# if entity['player'] in [Hand.us, Hand.them]:
	if entity['name'] == 'Mechanical Yeti':
		Hand.notes.append('Spare Part')
		Hand.draw(entity)

def discover(source):
	if source['player'] == Hand.them:
		if source['name'] == 'A Light in the Darkness':
			Hand.notes.append('A random minion with +1/+1')
		elif source['name'] == 'Dark Peddler':
			Hand.notes.append('A 1-cost card')
		elif source['name'] == 'Ethereal Conjurer':
			Hand.notes.append('A spell')
		elif source['name'] == 'Gorillabot A-3':
			Hand.notes.append('A mech')
		elif source['name'] == 'Jeweled Scarab':
			Hand.notes.append('A 3-cost card')
		elif source['name'] == 'Museum Curator':
			Hand.notes.append('A deathrattle card')
		elif source['name'] == 'Raven Idol':
			Hand.notes.append('A minion or a spell')
		elif source['name'] == 'Tomb Spider':
			Hand.notes.append('A beast')
		elif source['name'] == 'Journey Below':
			Hand.notes.append('A deathrattle card')
		elif source['name'] == 'Arch-Thief Rafaam':
			Hand.notes.append('A powerful artifact')
		elif source['name'] == 'Sir Finley Mrrgglton':
			return
		Hand.draw(source) # Not the real id of the discovered card, but ids aren't ever repeated anyways. Only a potential id duplicate with Brann.

def turnover(turn):
	global overload
	offset = 0 if Hand.wentFirst else 1
	if turn%2 == offset:
		if overload != 0:
			print 'Overload next turn:', overload
			overload = 0
