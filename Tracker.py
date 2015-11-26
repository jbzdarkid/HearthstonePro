'''Cards with special properties:
Dragon in hand: Blackwing Corruptor, Blackwing Technician, Twilight Welp, Alexstrasza's Champion, Wyrmrest Agent, Twilight Guardian, Chillmaw, Rend Blackhand
Spare Part:
Return to hand: Time Rewinder, Sap, Ancient Brewmaster, Anub'ar Ambusher, Dream, Freezing Trap, Shadowstep, Vanish, Youthful Brewmaster, Alarm-o-Bot, Coliseum Manager, Kidnapper, Anub'arak, The Skeleton Knight
Other: Sense Demons, Captain's Parrot, Cursed!, Golden Monkey, King's Elekk, Call Pet, Gnomish Experimenter, Holy Wrath, Varian Wrynn, Shadowfiend, Chromaggus, Flame Leviathan, Emperor Thaurissan, Headcrack
'''


hand = []

# Returns 1 if a > b, -1 if a < b, and 0 if a == b
def strcmp(a, b):
	if len(a) > len(b):
		return 1
	elif len(a) < len(b):
		return -1
	i = 0
	while a[i] == b[i]:
		i += 1
		if i == len(a):
			return 0
	if a[i] > b[i]:
		return 1
	elif a[i] < b[i]:
		return -1

# print strcmp('abc', 'abcd')
# print strcmp('abcd', 'abc')
# print strcmp('abce', 'abcd')
# print strcmp('abcd', 'abce')
# print strcmp('abcd', 'abcd')

# Remove elements from master. Both lists must be sorted!
def remove(master, toremove):
	i = j = 0
	while i < len(master) and j < len(toremove):
		comp = strcmp(master[i], toremove[j])
		if comp == -1:
			i += 1
			continue
		elif comp == 1:
			j += 1
			continue
		elif comp == 0:
			master.pop(i)
			j += 1
	return master

# master = ['a', 'b', 'c', 'd']
# print remove(['a', 'b', 'c', 'd'], ['a'])
# print remove(['a', 'b', 'c', 'd'], ['b', 'c'])
# print remove(master, ['d', 'e'])
# print master

class Card():
	def __init__(self, inHand=True, position=0, name=None, turn=0):
		self.name = name
		self.inHand = inHand
		self.position = position
		if self.turn == -1:
			self.turn = 0
			self.mulliganed = True
		else:
			self.turn = turn

	def __eq__(self, other):
		if type(other) is not type(self):
			return self.name == other # Allows comparison between Card() and string, but only in that order!
		elif self.name != other.name:
			return False
		elif self.inHand != other.inHand:
			return False
		elif self.position != other.position:
			return False
		elif self.turn != other.turn:
			return False
		return True

	def __ne__(self, other):
		return not self.__eq__(other)

	def isMinion(self):
		return self.name == 'Leper Gnome'

def draw(card):
	if len(hand) >= 10:
		raise Exception('Hand is full!')
	hand.append(card)

def play(slot):
	if slot >= len(hand) or slot < 0:
		raise Exception('Invalid slot')
	del hand[slot]

secrets = []

class Secret():
	def __init__(self, hero):
		if hero == 'Mage':
			self.possibleValues = ['Counterspell', 'Duplicate', 'Effigy', 'Ice Barrier', 'Ice Block', 'Mirror Entity', 'Spellbender', 'Vaporize']
		elif hero == 'Hunter':
			self.possibleValues = ['Bear Trap', 'Dart Trap', 'Explosive Trap', 'Freezing Trap', 'Misdirection', 'Snake Trap', 'Snipe']
		elif hero == 'Paladin':
			self.possibleValues = ['Avenge', 'Competitive Spirit', 'Eye for an Eye', 'Noble Sacrifice', 'Redemption', 'Repentance', 'Sacred Trial']
		else:
			raise Exception('Invalid hero')

	# Some relevant secret interactions:
	# Freezing trap will prevent Misdirection
	# Counterspell will prevent Spellbender
	# Explosive and bear ?

	# An action happened which did not trigger the secret. Eliminate secrets that would've triggered.
	# Ice block is not handled because that's irrelevant.
	def action(self, event):
		if event.owner != 'Us': # Secrets cannot trigger on their owner's turn. Competitive Spirit triggers on our turn end.
			return
		if event.kind == 'Attack':
			remove(self.possibleValues, ['Ice Barrier', 'Noble Sacrifice'])
			if event.target == 'Hero':
				remove(self.possibleValues, ['Bear Trap', 'Explosive Trap', 'Eye for an Eye', 'Misdirection'])
				if event.source != 'Hero':
					remove(self.possibleValues, ['Vaporize'])
			else:
				remove(self.possibleValues, ['Snake Trap'])
			if event.source != 'Hero':
				remove(self.possibleValues, ['Freezing Trap'])
		elif event.kind == 'Minion Died':
			remove(self.possibleValues, ['Avenge', 'Duplicate', 'Effigy', 'Redemption'])
		elif event.kind == 'Card Played' and event.source.isMinion():
			remove(self.possibleValues, ['Mirror Entity', 'Repentance', 'Snipe'])
			if event.minionCount() > 3:
				remove(self.possibleValues, ['Sacred Trial'])
		elif event.kind == 'Played Spell':
			remove(self.possibleValues, ['Counterspell'])
			if event.target:
				remove(self.possibleValues, ['Spellbender'])
		elif event.kind == 'Used Hero Power':
			remove(self.possibleValues, ['Dart Trap'])
		elif event.kind == 'Turn End': # And opp has creatures in play!
			remove(self.possibleValues, ['Competitive Spirit'])

class Event():
	# Args can contain up to 2 elements.
	# Event.source and Event.target should always be Card() instances.
	def __init__(self, kind, owner, *args):
		if kind not in ['Card Played', 'Life Gained', 'Life Lost', 'Turn End', 'Minion Died', 'Attack', 'Secret Triggered']:
			raise Exception('Invalid event type:', kind)
		self.kind = kind
		if owner not in ['Us', 'Them']:
			raise Exception('Unknown event owner:', owner)
		self.owner = owner
		if kind == 'Attack':
			self.source = args[0]
			self.target = args[1]
		elif kind == 'Life Gained' or kind == 'Life Lost':
			self.amount = args[0]
		elif kind == 'Minion Died':
			self.source = args[0]
		elif kind == 'Card Played':
			self.source = args[0]
			if len(args) > 1:
				self.target = args[1]
		elif kind == 'Secret Triggered':
			secrets.pop(args[0])
