# Displaying with tk:
# Use Toplevel() in construction, and root.lift() as a backup

'''Cards with special properties:
Dragon in hand: Blackwing Corruptor, Blackwing Technician, Twilight Welp, Alexstrasza's Champion, Wyrmrest Agent, Twilight Guardian, Chillmaw, Rend Blackhand
Spare Part:
Return to hand: Ancient Brewmaster, Anub'ar Ambusher, Dream, Freezing Trap, Shadowstep, Vanish, Youthful Brewmaster, Alarm-o-Bot, Coliseum Manager, Kidnapper, Anub'arak, The Skeleton Knight
Other: Cursed!, Golden Monkey, King's Elekk, Gnomish Experimenter, Holy Wrath, Varian Wrynn, Shadowfiend, Chromaggus, Flame Leviathan, Emperor Thaurissan, Headcrack, Unstable Portal, Wild Growth, Mulch, Vanish, Echo of Mediv,
'''

class card():
	def __init__(self, id):
		global turn, notes
		self.id = id
		self.turn = turn/2
		self.notes = (notes.pop()+' ') if len(notes) > 0 else ''

	# def __repr__(self):
	# 	print 'card(%s)' % (self.id)

def reset():
	global turn, hand, notes, wentFirst, us, them
	turn = 0
	hand = []
	notes = [] # Push to this to signal information about the next draw.
	wentFirst = 0
	us = '0' # player id
	them = '0' # player id

reset()

def draw(entity, position):
	global hand, wentFirst
	if entity['player'] == them:
		print '<33>', hand, entity['id']
		id = int(entity['id'])
		if turn == 0 and id == 68:
			notes.append('The Coin')
			wentFirst = 1
		# Extend hand. [None]*-2 = [], so this won't extend unnecessarily.
		hand.extend([None]*(position - len(hand) + 1))
		hand[position] = card(id)

# When a card is removed from a player's hand
def play(entity):
	global hand
	if entity['player'] == them:
		print '<45>', hand, entity['id']
		hand.pop(int(entity['zonePos'])-1)
		print '<47>', hand

# When a card hits the board
def play2(entity):
	if entity['player'] == them:
		if entity['name'] == 'Unstable Portal':
			notes.append('Drawn from Unstable Portal')
			draw(card(-1))
		elif entity['name'] == 'Toshley':
			notes.append('Spare Part')

def die(entity):
	if entity['player'] == them:
		if entity['name']	== 'Clockwork Gnome':
			notes.append('Spare Part')
	if entity['name'] == 'Mechanical Yeti':
		notes.append('Spare Part')

# Cards that are mulliganed have the same id as the original cards, so for all intents and purposes, I treat them as the same card.
# The Innkeeper will mulligan every card in their hand, including the coin. Magic!
def mulligan(entity):
	global hand
	if entity['player'] == them:
		print hand
		index = int(entity['zonePos'])-1
		hand[index].notes += 'Mulliganed '
		print hand

def turnover():
	global turn, hand, wentFirst
	turn += 1
	if (turn+wentFirst)%2 == 0:
		print 'Current Turn:', turn/2
		print 'Card No. | Turn | Notes'
		for i in range(len(hand)):
			print ' %s | %s | %s' % ('%d'.ljust(9) % (i+1), '%d'.ljust(6) % hand[i].turn, ' %s' % hand[i].notes)

def length():
	global hand
	return len(hand)
