# Displaying with tk:
# Use Toplevel() in construction, and root.lift() as a backup

'''Cards with special properties:
Dragon in hand: Blackwing Corruptor, Blackwing Technician, Twilight Welp, Alexstrasza's Champion, Wyrmrest Agent, Twilight Guardian, Chillmaw, Rend Blackhand
Spare Part:
Return to hand: Ancient Brewmaster, Anub'ar Ambusher, Dream, Freezing Trap, Shadowstep, Vanish, Youthful Brewmaster, Alarm-o-Bot, Coliseum Manager, Kidnapper, Anub'arak, The Skeleton Knight
Other: Cursed!, Golden Monkey, King's Elekk, Gnomish Experimenter, Holy Wrath, Varian Wrynn, Shadowfiend, Chromaggus, Flame Leviathan, Emperor Thaurissan, Headcrack, Unstable Portal, Wild Growth, Mulch
'''

class card():
	def __init__(self, name, mulligan=False):
		global turn
		self.name = name
		self.turn = turn/2
		self.mulligan = mulligan

	def __repr__(self):
		print 'card(%s%s)' % (self.name, 'mulligan=True' if self.mulligan else '')

turn = 0
hand = []
names = [None]*64
wentFirst = 0

def reset():
	global turn, hand, names, wentFirst
	wentFirst = 0
	turn = 0
	hand = []
	names = [None]*64

reset()

def draw(id):
	global hand
	hand.append(card(id))

def play(pos):
	global hand
	card = hand.pop(pos)
	print card

	if card.name == 'Unstable Portal':
		print '<56>'

def mulligan(pos, id):
	global hand
	if hand[pos].name != id:
		hand[pos] = card(id, mulligan=True)

def turnover():
	global turn, hand, wentFirst
	turn += 1
	if (turn+wentFirst)%2 == 0:
		print 'Current Turn:', turn/2
		print 'Card No. | Drawn on turn | Name | Other notes'
		for i in range(len(hand)):
			print '       %d |            %02d |  %s |' % (i, hand[i].turn, str(hand[i].name))

def length():
	global hand
	return len(hand)
