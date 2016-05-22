import Hand, Cards
# Main parsing function. line_generator can be a tail for live execution, or a file object for testing.
def parseFile(line_generator, config):
	for line in line_generator():
		line = line[19:] # Strips out timestamp
		if line[:40] == 'GameState.DebugPrintPower() - TAG_CHANGE':
			data = parse(line[40:])
			if data['tag'] == 'PLAYER_ID':
				if data['Entity'] == config['username']:
					Hand.us = data['value']
				else:
					Hand.them = data['value']
			elif data['tag'] == 'FIRST_PLAYER':
				Hand.wentFirst(data['Entity'] == config['username'])
		if line[:49] == 'GameState.DebugPrintEntitiesChosen() -   Entities': # Cards that were not mulliganed
			entity = parse(line[54:-2])
			Hand.keep(entity)
		if line[:45] == 'PowerTaskList.DebugPrintPower() - BLOCK_START':
			data = parse(line[45:])
			if data['BlockType'] == 'TRIGGER':
				if 'zone' in data['Entity'] and data['Entity']['zone'] == 'GRAVEYARD':
					Cards.die(data['Entity'])
		# if line[:49] == 'PowerTaskList.DebugPrintPower() -     SHOW_ENTITY':
		# 	data = parse(line[52:])
		# 	Hand.discard(data['Entity'])
		if line[:46] == 'GameState.DebugPrintEntityChoices() -   Source':
			data = parse(line[40:])
			if data['Source'] != 'GameEntity': # Not the mulligan choices
				Cards.discover(data['Source'])
		if line[:49] == 'PowerTaskList.DebugPrintPower() -     HIDE_ENTITY':
			print '<26>', line[49:]
		if line[:45] == 'PowerTaskList.DebugPrintPower() - BLOCK_START':
			data = parse(line[46:])
			if data['BlockType'] == 'POWER':
				Cards.play2(data['Entity']) # When a card actually hits the board
		if line[:48] == 'PowerTaskList.DebugPrintPower() -     TAG_CHANGE':
			data = parse(line[48:])
			if data['tag'] == 'ZONE_POSITION':
				if 'zone' in data['Entity'] and data['Entity']['zone'] == 'DECK':
					Hand.draw(data['Entity'], int(data['value'])-1)
			elif data['tag'] == 'JUST_PLAYED':
				if data['Entity']['zone'] == 'HAND':
					Hand.play(data['Entity']) # When a card is removed from a player's hand
			elif data['tag'] == 'TURN':
				Cards.turnover(int(data['value']))
				Hand.turnover(int(data['value']))
			elif data['tag'] == 'STEP':
				if data['value'] == 'FINAL_GAMEOVER':
					Hand.reset()
					print 'Game Over'

# Setup scripts.
if __name__ == '__main__':
	from ast import literal_eval
	from os import sep
	from os.path import expanduser
	from subprocess import Popen, PIPE

	try:
		config = literal_eval(open('config.cfg', 'rb').read())
	except IOError:
		# Config not defined, somehow. Recreate.
		config = {}
	except SyntaxError:
		# Config corrupt, somehow. Recreate.
		config = {}

	if any(key not in config for key in ['logconfig', 'log', 'username']):
		print 'Config incomplete or corrupted, (re)generating. This might take a while...'
		from platform import system
		from os import walk
		if system() == 'Windows':
			config['logconfig'] = '%LocalAppData%'
		elif system() == 'Darwin': # Mac OSX
			config['logconfig'] = expanduser('~')+'/Library/Preferences'
			appName = 'Hearthstone.app'
		else:
			raise Exception('Unknown platform:', system())
		config['logconfig'] += '/Blizzard/Hearthstone/log.config'

		for root, dirs, files in walk(expanduser('~')):
			if appName in dirs+files:
				config['log'] = root + sep + 'Logs' + sep
				if 'username' in config:
					break
			if root.rsplit(sep)[-1] == 'Logs':
				for f in files:
					if 'battle.net' in f:
						from re import search
						f = open(root+sep+files[0]).read()
						m = search('m_battleTag: (.*?)#', f)
						config['username'] = m.group(1)
						break
				if 'log' in config and 'username' in config:
					break

	c = open('config.cfg', 'wb')
	c.write(str(config))
	c.close()

	f = open('log.config', 'rb').read()
	try:
		g = open(config['logconfig'], 'rb').read()
		if f != g:
			# Config exists, but differs
			g = open(config['logconfig'], 'wb')
			g.write(f)
			g.close()
		# Config exists, same
	except IOError:
		# Config doesn't exist
		g = open(config['logconfig'], 'wb')
		g.write(f)
		g.close()

	def debug(string):
		# print string
		return

	# Python throws some errors here about 'key not defined'. It is defined in the data[i] = '=' block, which will be called (on properly formatted input) before 'key' is referenced.
	# There are scenarios where this error will be thrown during execution, but only on invalid log data.
	def parse(data, start=0):
		data = data.strip()
		debug(data)
		out = {}
		index = start
		possible = start
		i = start
		recursed = True
		while i < len(data):
			debug(str(i)+' '+str(data[i]))
			if data[i] == '[':
				debug('Recursing...')
				out[key], i = parse(data, i+1)
				possible = start
				recursed = True
				debug('Recursion returned: '+str(out[key]))
			elif data[i] == ']':
				value = data[index:i]
				debug('<1>Value: data['+str(index)+':'+str(i)+']='+str(value))
				out[key] = value
				return (out, i)
			elif data[i] == ' ':
				possible = i+1
				debug('Possible key: data['+str(i+1)+':'+str(i+2)+']='+str(data[i+1:i+2]))
			elif data[i] == '=':
				if not recursed:
					out[key] = data[index:possible-1]
					debug('<2>Value: data['+str(index)+':'+str(possible-1)+']='+str(out[key]))
				key = data[possible:i]
				debug('Key: data['+str(possible)+':'+str(i)+']='+str(key))
				index = i+1
				recursed = False
			i += 1
		if not recursed: # The last k,v pair
			out[key] = data[index:]
			debug('<3>Value: data['+str(index)+':]='+str(out[key]))
		return out

	# print '1', parse('')
	# print '2', parse('a=b')
	# print '3', parse('a=b c')
	# print '4', parse('a=[b=c]')
	# print '5', parse('a=b c=d')
	# print '6', parse('a=[b=c d]')
	# print '7', parse('a=[b=c] d=e')
	# print '8', parse('a=[b=c d=e]')
	# print '9', parse('a=b c d=e')
	# print '0', parse('a=b c=[d=e] f=g')
	# print 'A', parse('a=[b=c d=e] f=g')

	print 'Startup complete.'

	def tail():
		tail = Popen(['tail', '-f', config['log']+'Power.log'], stdout=PIPE)
		while True:
			yield tail.stdout.readline()

	parseFile(tail, config)
