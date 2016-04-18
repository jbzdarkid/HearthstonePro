from ast import literal_eval
from os import sep
from os.path import expanduser
from subprocess import Popen, PIPE
import Hand, Secret

try:
	config = literal_eval(open('config.cfg', 'rb').read())
except IOError:
	# Config not defined, somehow. Recreate.
	config = {}
except SyntaxError:
	# Config corrupt, somehow. Recreate.
	config = {}

if 'logconfig' not in config:
	from platform import system
	if system() == 'Windows':
		config['logconfig'] = '%LocalAppData%'
	elif system() == 'Darwin': # Mac OSX
		config['logconfig'] = expanduser('~')+'/Library/Preferences'
		name = 'Hearthstone.app'
	else:
		raise Exception('Unknown platform:', system())
	config['logconfig'] += '/Blizzard/Hearthstone/log.config'

if 'log' not in config:
	from os import walk
	for root, dirs, files in walk(expanduser('~')):
		if name in dirs+files:
			config['log'] = root + sep + 'Logs' + sep
	if 'log' not in config:
		raise Exception('Couldn\'t find Hearthstone install!')
	print config['log']

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

tail = Popen(['tail', '-f', config['log']+'Power.log'], stdout=PIPE)
while True:
	line = tail.stdout.readline()
	line = line[19:] # Strips out timestamp
	# Start of game player id assignment
	if line[:40] == 'GameState.DebugPrintPower() - TAG_CHANGE':
		data = parse(line[40:])
		if data['tag'] == 'PLAYER_ID':
			if data['Entity'] == 'darkid':
				Hand.us = data['value']
				Secret.us = data['value']
			else:
				Hand.them = data['value']
				Secret.them = data['value']

	if line[:48] == 'GameState.DebugPrintEntityChoices() -   Entities': # Initial cards in hand
		data = parse(line[53:-2])
		Hand.draw(data)
	if line[:49] == 'GameState.DebugPrintEntitiesChosen() -   Entities': # Cards that were mulliganed
		data = parse(line[54:-2])
		Hand.mulligan(data)

	if line[:46] == 'PowerTaskList.DebugPrintPower() - ACTION_START':
		data = parse(line[46:])
		if data['BlockType'] == 'POWER': # When a card actually hits the board
			Hand.play2(data['Entity'])
	if line[:48] == 'PowerTaskList.DebugPrintPower() -     TAG_CHANGE':
		data = parse(line[48:])
		if data['tag'] == 'ZONE_POSITION':
			if 'zone' in data['Entity'] and data['Entity']['zone'] == 'DECK': # Drew a card
				Hand.draw(data['Entity'])
		elif data['tag'] == 'JUST_PLAYED':
			if data['Entity']['zone'] == 'HAND': # When a card is removed from a player's hand
				Hand.play(data['Entity'])
		elif data['tag'] == 'ZONE':
			if 'zone' in data['Entity']:
				if data['Entity']['zone'] == 'SECRET':
					if data['Entity']['player'] == '2':
						Secret.trigger(data['Entity']['name'], int(data['Entity']['zonePos']))
		elif data['tag'] == 'TURN': # End of turn
			Hand.turnover()
			Secret.turnover()
		elif data['tag'] == 'STEP':
			if data['value'] == 'FINAL_GAMEOVER': # End of game
				Hand.reset()
				Secret.reset()
				print 'Game Over'
