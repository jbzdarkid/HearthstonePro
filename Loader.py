from ast import literal_eval
from os import sep
from os.path import expanduser
from subprocess import Popen, PIPE

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
			self.source = args[0]

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
except IOError, e:
	# Config doesn't exist
	g = open(config['logconfig'], 'wb')
	g.write(f)
	g.close()

def debug(string):
	# print string
	return

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

player_ids = [64, 66]
player_health = [30, 30]
metadata = 0
game_start = -1

tail = Popen(['tail', '-f', config['log']+'Power.log'], stdout=PIPE)
meta_lines = 0
while True:
	line = tail.stdout.readline()
	function = line[19:line.find('.', 20)]
	line = line.split('()', 1)[1][3:]
	if line[:18] == '        GameEntity':
		print 'New game started.'
		game_start = 0
	elif game_start >= 0:
		if line[:15] == '    FULL_ENTITY':
			game_start = -1
		elif line[:14] == '        Player':
			data = parse(line[15:])
			print data
			game_start = int(data['PlayerID'])
		else:
			data = parse(line)
			if data['tag'] == 'HERO_ENTITY':
				player_ids[game_start-1] = data['value']
	elif line[:10] == '  Entities':
		print '<134>', line[15:-2]
		data = parse(line[15:-2])
		if 'name' in data:
			print 'Initial card '+line[12]+': '+data['name']
	elif line[:12] == 'ACTION_START' and function == 'PowerTaskList':
		data = parse(line[13:])
		if data['BlockType'] == 'POWER':
			print 'Player', data['Entity']['player'], 'played', data['Entity']['name'],
			if data['Target'] != '0':
				print 'targeting', data['Target']['name']
			else:
				print ''
		elif data['BlockType'] == 'ATTACK':
			print 'Player', data['Entity']['player'], 'attacked', data['Target']['name'], 'with', data['Entity']['name']
		elif data['BlockType'] == 'TRIGGER' and data['Index'] != '-1':
			print '<150>', data
	elif line[:13] == '    META_DATA':
		data = parse(line[16:])
		metadata = int(data['Info'])
	elif metadata > 0:
		metadata -= 1
		id = parse(line[19:-2])['id']
		if data['Meta'] == 'DAMAGE':
			if player_ids[0] == id:
				player_health[0] -= int(data['Data'])
			elif player_ids[1] == id:
				player_health[1] -= modifier*int(data['Data'])
		elif data['Meta'] == 'HEALING':
			if player_ids[0] == id:
				player_health[0] += int(data['Data'])
			elif player_ids[1] == id:
				player_health[1] += modifier*int(data['Data'])
		if id in player_ids:
			if data['Meta'] == 'DAMAGE':
				player_health[player_ids.index(id)] -= int(data['Data'])
			elif data['Meta'] == 'HEALING':
				player_health[player_ids.index(id)] += int(data['Data'])
			else:
				continue
			print 'Health:', player_health[0], '(you)', player_health[1], '(them)'
	elif line[:14] == '    TAG_CHANGE':
		data = parse(line[15:])
		if 'zone' in data['Entity'] and data['Entity']['zone'] == 'SECRET':
			print '<166>', data
	elif line[:10] == 'TAG_CHANGE':
		pass
	elif line[:17] == 'm_currentTaskList':
		pass
	elif line[:10] == 'End Action':
		pass
	elif line[:10] == 'ACTION_END':
		pass
	elif line[:13] == 'Source Action':
		pass
	# else:
		# print line[:50]