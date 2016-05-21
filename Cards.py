# Dragons: Blackwing Corruptor, Blackwing Technician, Twilight Whelp, Alextrasza's Champion, Wyrmrest Agent, Twilight Guardian, Rend Blackhand, Chillmaw
# Deathrattle: Clockwork Gnome, Mechanical Yeti, Tomb Pillager, Webspinner, Infest*, Shifting Shade, Undercity Huckster, Rhonin, Toshley, Xaril. Poisoned Mind
# Shadowstep effects: Bloodthistle Toxin, Dream, Time Rewinder, Sap, Ancient Brewmaster, Anub'ar Ambusher, Freezing Trap, Shadowstep, Vanish*, Youthful Brewmaster, Alarm-o-Bot, Coliseum Manager, Kidnapper, Tentacles for Arms, Anub'arak, The Skeleton Knight
# Important specific cards: King's Elekk, Sea Reaver, Flame Leviathan, Holy Wrath, Varian Wrynn, Ancient Harbinger, Nefarian, Archmage Antonidas, Ysera, Chromaggus, Unstable Portal
# Unimportant specific cards: Call Pet, Gnomish Experimenter, Thistle Tea, Far Sight, Sense Demons, Captain's Parrot, Headcrack, Trade Prince Gallywix, Lorewalker Cho

import Hand

def reset():
	global overload
	overload = 0

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

		# if entity['name'] == 'Unstable Portal':
		# 	Hand.notes.append('Random minion that costs 3 less')
		# 	Hand.draw(entity)
		# elif entity['name'] == 'Toshley':
		# 	Hand.notes.append('Spare Part')
		#		Hand.draw(entity)

def die(entity):
	if entity['player'] == Hand.them:
		if entity['name']	== 'Clockwork Gnome':
			Hand.notes.append('Spare Part')
			Hand.draw(entity)
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

def turnover():
	global overload
	offset = 0 if Hand.us == '2' else 1
	if Hand.turn%2 == offset:
		if overload != 0:
			print 'Overload next turn:', overload
			overload = 0
