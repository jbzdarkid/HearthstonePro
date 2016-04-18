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
		self.notes = notes.pop() if len(notes) > 0 else ''

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

def draw(entity):
	global hand, wentFirst
	if entity['player'] == them:
		id = int(entity['id'])
		hand.append(card(id))
		if turn == 0 and id == 68:
			hand[4].notes = 'The Coin '
			wentFirst = 1

# When a card is removed from a player's hand
def play(entity):
	global hand
	if entity['player'] == them:
		hand.pop(int(entity['zonePos'])-1)

# When a card hits the board
def play2(entity):
	if entity['player'] == them:
		if entity['name'] == 'Unstable Portal':
			notes.append('Costs (3) less')
		elif entity['name'] == 'Toshley':
			notes.append('Spare Part')

# Cards that are mulliganed have the same id as the original cards, so for all intents and purposes, I treat them as the same card.
def mulligan(entity):
	global hand
	if entity['player'] == them:
		hand[int(entity['zonePos'])-1].notes += 'Mulliganed '

def turnover():
	global turn, hand, wentFirst
	turn += 1
	if (turn+wentFirst)%2 == 0:
		print 'Current Turn:', turn/2
		print 'Card No. | Turn | Notes'
		for i in range(len(hand)):
			print '%s|%s|%s' % ('%d '.rjust(10) % (i+1), '%d '.rjust(7) % hand[i].turn, '%s '.rjust(15) % hand[i].notes)

def length():
	global hand
	return len(hand)
