# Displaying with tk:
# Use Toplevel() in construction, and root.lift() as a backup

# Dragons: Blackwing Corruptor, Blackwing Technician, Twilight Whelp, Alextrasza's Champion, Wyrmrest Agent, Twilight Guardian, Rend Blackhand, Chillmaw
# Deathrattle: Clockwork Gnome, Mechanical Yeti, Tomb Pillager, Webspinner, Infest*, Shifting Shade, Undercity Huckster, Rhonin, Toshley, Xaril. Poisoned Mind
# Shadowstep effects: Bloodthistle Toxin, Dream, Time Rewinder, Sap, Ancient Brewmaster, Anub'ar Ambusher, Freezing Trap, Shadowstep, Vanish*, Youthful Brewmaster, Alarm-o-Bot, Coliseum Manager, Kidnapper, Tentacles for Arms, Anub'arak, The Skeleton Knight
# Important specific cards: King's Elekk, Sea Reaver, Flame Leviathan, Holy Wrath, Varian Wrynn, Ancient Harbinger, Nefarian, Archmage Antonidas, Ysera, Chromaggus
# Unimportant specific cards: Call Pet, Gnomish Experimenter, Thistle Tea, Far Sight, Sense Demons, Captain's Parrot, Headcrack, Trade Prince Gallywix, Lorewalker Cho

class card():
	def __init__(self, id):
		global turn, notes
		self.id = id
		self.turn = turn/2
		self.notes = (notes.pop()+' ') if len(notes) > 0 else ''

	def __repr__(self):
		return 'card(%s)' % (self.id)

def reset():
	global turn, hand, notes, us, them
	turn = 0
	hand = []
	notes = [] # Push to this to signal information about the next draw.
	us = '0' # player id
	them = '0' # player id

reset()

def wentFirst(truth):
	global us, them, notes, hand
	if truth:
		us = '1'
		them = '2'
		notes = ['The Coin', 'Mulliganned', 'Mulliganned', 'Mulliganned', 'Mulliganned']
		hand = [card(-1) for _ in range(5)]
	else:
		us = '2'
		them = '1'
		notes = ['Mulliganned', 'Mulliganned', 'Mulliganned']
		hand = [card(-1) for _ in range(3)]

def discover(source):
	global notes
	if source['player'] == them:
		if source['name'] == 'A Light in the Darkness':
			notes.append('A random minion with +1/+1')
		elif source['name'] == 'Dark Peddler':
			notes.append('A 1-cost card')
		elif source['name'] == 'Ethereal Conjurer':
			notes.append('A spell')
		elif source['name'] == 'Gorillabot A-3':
			notes.append('A mech')
		elif source['name'] == 'Jeweled Scarab':
			notes.append('A 3-cost card')
		elif source['name'] == 'Museum Curator':
			notes.append('A deathrattle card')
		elif source['name'] == 'Raven Idol':
			notes.append('A minion or a spell')
		elif source['name'] == 'Tomb Spider':
			notes.append('A beast')
		elif source['name'] == 'Journey Below':
			notes.append('A deathrattle card')
		elif source['name'] == 'Arch-Thief Rafaam':
			notes.append('A powerful artifact')
		elif source['name'] == 'Sir Finley Mrrgglton':
			return
		draw(source['id']) # Not the real id of the discovered card, but ids aren't ever repeated anyways. Only a potential id duplicate with Brann.

def draw(entity, position=None):
	global hand, them
	if entity['player'] == them:
		# Ovewriting a card because it was mulliganned
		if position < len(hand):
			hand[position].id = entity['id']
		else:
			hand.append(card(int(entity['id'])))

# When a card is removed from a player's hand
def play(entity):
	global hand
	if entity['player'] == them:
		hand.pop(int(entity['zonePos'])-1)

# When a card hits the board, and we can see what it's name is
def play2(entity):
	global them, overload
	if entity['player'] == them:
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
		# 	notes.append('Random minion that costs 3 less')
		# 	draw(card(-1))
		# elif entity['name'] == 'Toshley':
		# 	notes.append('Spare Part')

def die(entity):
	if entity['player'] == them:
		if entity['name']	== 'Clockwork Gnome':
			notes.append('Spare Part')
			hand.draw(entity['id'])
	if entity['name'] == 'Mechanical Yeti':
		notes.append('Spare Part')
		hand.draw(entity['id'])

# The mulligan works backwards, with cards that are kept appearing in the log file. Thus I initialize the cards in hand to be 'Mulliganned', and replace them if they appear.
def keep(entity):
	global hand
	if entity['player'] == them:
		print '<79>', entity, hand
		hand[int(entity['zonePos'])-1] = card(entity['id'])

def turnover():
	global turn, hand, overload
	turn += 1
	offset = 0 if us == '2' else 1
	if turn%2 == offset:
		print 'Current Turn:', turn/2
		if overload != 0:
			print 'Overload next turn:', overload
			overload = 0
		print 'Card No. | Turn | Notes'
		for i in range(len(hand)):
			print ' %s | %s | %s' % ('%d'.ljust(8) % (i+1), '%d'.ljust(5) % hand[i].turn, ' %s' % hand[i].notes)

def length():
	global hand
	return len(hand)
