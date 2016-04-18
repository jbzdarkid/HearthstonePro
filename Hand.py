# Displaying with tk:
# Use Toplevel() in construction, and root.lift() as a backup

'''Cards with special properties:
Dragon in hand: Blackwing Corruptor, Blackwing Technician, Twilight Welp, Alexstrasza's Champion, Wyrmrest Agent, Twilight Guardian, Chillmaw, Rend Blackhand
Spare Part:
Return to hand: Ancient Brewmaster, Anub'ar Ambusher, Dream, Freezing Trap, Shadowstep, Vanish, Youthful Brewmaster, Alarm-o-Bot, Coliseum Manager, Kidnapper, Anub'arak, The Skeleton Knight
Other: Cursed!, Golden Monkey, King's Elekk, Gnomish Experimenter, Holy Wrath, Varian Wrynn, Shadowfiend, Chromaggus, Flame Leviathan, Emperor Thaurissan, Headcrack, Unstable Portal, Wild Growth, Mulch, Vanish, Echo of Mediv, 
'''

class card():
	def __init__(self, id, mulligan=False):
		global turn, notes
		self.id = id
		self.turn = turn/2
		self.notes = notes.pop() if len(notes) > 0 else ''
		self.mulligan = mulligan

	# def __repr__(self):
	# 	print 'card(%s%s)' % (self.id, 'mulligan=True' if self.mulligan else '')

def reset():
	global turn, hand, notes, wentFirst
	turn = 0
	hand = []
	notes = [] # Push to this to signal information about the next draw.
	wentFirst = 0

reset()

def draw(id):
	print 'Drew card', id
	global hand
	hand.append(card(id))

# When a card is removed from a player's hand
def play(pos, id):
	print 'Played card #%d: %s' % (pos, id)
	global hand
	hand.pop(pos)

# When a card hits the board
def play2(name, player):
	if player == 2:
		if name == 'Unstable Portal':
			notes.append('Costs (3) less')

def mulligan(pos, id):
	global hand
	if hand[pos].id != id:
		hand[pos] = card(id, mulligan=True)

def turnover():
	global turn, hand, wentFirst
	turn += 1
	if (turn+wentFirst)%2 == 0:
		print 'Current Turn:', turn/2
		print 'Card No. | Turn | Notes'
		for i in range(len(hand)):
			print '%s|%s|%s' % ('%d '.rjust(10) % i, '%d '.rjust(7) % hand[i].turn, '%s '.rjust(15) % hand[i].notes)

def length():
	global hand
	return len(hand)
