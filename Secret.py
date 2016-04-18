
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

secrets = []

class Secret():
	def __init__(self, hero):
		if hero == 'Mage':
			self.possibleValues = [
				'Counterspell',
				'Duplicate',
				'Effigy',
				'Ice Barrier',
				'Ice Block',
				'Mirror Entity',
				'Spellbender',
				'Vaporize'
			]
		elif hero == 'Hunter':
			self.possibleValues = [
				'Bear Trap',
				'Dart Trap',
				'Explosive Trap',
				'Freezing Trap',
				'Misdirection',
				'Snake Trap',
				'Snipe'
			]
		elif hero == 'Paladin':
			self.possibleValues = [
				'Avenge',
				'Competitive Spirit',
				'Eye for an Eye',
				'Noble Sacrifice',
				'Redemption',
				'Repentance',
				'Sacred Trial'
			]
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
		elif event.kind == 'Secret Triggered':
			remove(self.possibleValues, [event.args[0]])
