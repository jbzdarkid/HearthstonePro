from ast import literal_eval
from os import sep
from os.path import expanduser
from subprocess import Popen, PIPE
import Hand

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
	line = line[19:]
	# Initial hand
	if line[:48] == 'GameState.DebugPrintEntityChoices() -   Entities':
		data = parse(line[53:-2])
		if data['player'] == '2':
			if Hand.length() == 4:
				Hand.draw(68)
				Hand.associate(68, 'The Coin')
				Hand.wentFirst = 1
			else:
				Hand.draw(int(data['id']))
	# Hand after mulligan
	if line[:49] == 'GameState.DebugPrintEntitiesChosen() -   Entities':
		data = parse(line[54:-2])
		if data['player'] == '2':
			Hand.mulligan(int(data['zonePos'])-1, data['id'])
	if line[:48] == 'PowerTaskList.DebugPrintPower() -     TAG_CHANGE':
		data = parse(line[48:])
		if 'Entity' in data and 'name' in data['Entity']:
			Hand.associate(int(data['Entity']['id']), data['Entity']['name'])

		# Drew a card
		if data['tag'] == 'ZONE_POSITION':
			if 'zone' in data['Entity'] and data['Entity']['zone'] == 'DECK':
				if data['Entity']['player'] == '2':
					Hand.draw(int(data['Entity']['id']))
		# Played a card
		elif data['tag'] == 'JUST_PLAYED':
			if data['Entity']['zone'] == 'HAND':
				if data['Entity']['player'] == '2':
					Hand.play(int(data['Entity']['zonePos'])-1)
		# End of turn
		elif data['tag'] == 'TURN':
			Hand.turnover()
		elif data['tag'] == 'STEP':
			if data['value'] == 'FINAL_GAMEOVER':
				Hand.reset()
				print 'Game Over'
