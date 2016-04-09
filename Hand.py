# Displaying with tk:
# Use Toplevel() in construction, and root.lift() as a backup

'''Cards with special properties:
Dragon in hand: Blackwing Corruptor, Blackwing Technician, Twilight Welp, Alexstrasza's Champion, Wyrmrest Agent, Twilight Guardian, Chillmaw, Rend Blackhand
Spare Part:
Return to hand: Ancient Brewmaster, Anub'ar Ambusher, Dream, Freezing Trap, Shadowstep, Vanish, Youthful Brewmaster, Alarm-o-Bot, Coliseum Manager, Kidnapper, Anub'arak, The Skeleton Knight
Other: Cursed!, Golden Monkey, King's Elekk, Gnomish Experimenter, Holy Wrath, Varian Wrynn, Shadowfiend, Chromaggus, Flame Leviathan, Emperor Thaurissan, Headcrack, Unstable Portal, Wild Growth, Mulch
'''

class card():
	def __init__(self, id, mulligan=False):
		global turn
		self.id = id
		self.turn = turn/2
		self.mulligan = mulligan

	def name(self):
		if names[self.id] != '':
			return names[self.id]
		else:
			return self.id

	# def __repr__(self):
	# 	print 'card(%s%s)' % (self.id, 'mulligan=True' if self.mulligan else '')

turn = 0
hand = []
names = [None]*128
wentFirst = 0

def reset():
	global turn, hand, names, wentFirst
	wentFirst = 0
	turn = 0
	hand = []
	names = [None]*128

reset()

def draw(id):
	global hand
	hand.append(card(id))

def play(pos):
	global hand
	card = hand.pop(pos)

def mulligan(pos, id):
	global hand
	if hand[pos].id != id:
		hand[pos] = card(id, mulligan=True)

def associate(id, name):
	global names
	print 'Associating', id, name
	names[id] = name

def turnover():
	global turn, hand, wentFirst
	turn += 1
	if (turn+wentFirst)%2 == 0:
		print 'Current Turn:', turn/2
		print 'Card No. | Turn | Name          | Other notes'
		for i in range(len(hand)):
			print '%s|%s|%s|%s' % ('%d '.rjust(10) % i, '%d '.rjust(7) % hand[i].turn, '%s '.rjust(15) % hand[i].name(), '')

def length():
	global hand
	return len(hand)
