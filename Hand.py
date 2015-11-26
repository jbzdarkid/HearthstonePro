'''Cards with special properties:
Dragon in hand: Blackwing Corruptor, Blackwing Technician, Twilight Welp, Alexstrasza's Champion, Wyrmrest Agent, Twilight Guardian, Chillmaw, Rend Blackhand
Spare Part:
Return to hand: Ancient Brewmaster, Anub'ar Ambusher, Dream, Freezing Trap, Shadowstep, Vanish, Youthful Brewmaster, Alarm-o-Bot, Coliseum Manager, Kidnapper, Anub'arak, The Skeleton Knight
Other: Cursed!, Golden Monkey, King's Elekk, Gnomish Experimenter, Holy Wrath, Varian Wrynn, Shadowfiend, Chromaggus, Flame Leviathan, Emperor Thaurissan, Headcrack, Unstable Portal, Wild Growth, Mulch
'''

hand = []
toDraw = []

class Card():
	def __init__(self, position=0, name=None, turn=0):
		self.position = position
		self.name = name
		if self.turn == -1:
			self.turn = 0
			self.mulliganed = True
		else:
			self.turn = turn
		self.notes = ''

	def __eq__(self, other):
		if type(other) is not type(self):
			return self.name == other # Allows comparison between Card() and string, but only in that order!
		elif self.name != other.name:
			return False
		elif self.position != other.position:
			return False
		elif self.turn != other.turn:
			return False
		return True

	def __ne__(self, other):
		return not self.__eq__(other)

	def addNote(self, note):
		self.notes += '\n'+note

def draw():
	card = new Card()
	if len(toDraw) > 0:
		card.setNote('Drawn by'+toDraw.pop(0))
	hand.append(new Card())

def processCardPlayed(event):
	if event.kind != 'Card Played':
		return
	if event.source in ['Time Rewinder', 'Sap']:
		toDraw += [event.target]
	elif event.source == 'Emperor Thaurissan':
		for card in hand:
			card.addNote('Cost reduced by 1 by Emperor Thaurissan')
	elif event.source == 'Sense Demons':
		toDraw += [played.name]*2
	elif event.source in ['Captain's Parrot', 'Call Pet']:
		toDraw += [played.name]