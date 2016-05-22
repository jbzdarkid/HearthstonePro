from sys import argv
from os import getcwd, sep
import Parser

def line_generator(file):
	global lineNo
	lineNo = 0
	f = open(file, 'rb')
	for line in f:
		yield line
		lineNo += 1

if len(argv) == 1 or argv[1] == 'all':
	from os import listdir
	files = listdir('tests')
# elif argv[1] == 'latest':
#   from os.path import getmtime
else:
	files = argv[1:]

config = {'username':'darkid'}
for file in files:
	fullName = getcwd()+sep+'tests'+sep+file
	try:
		Parser.parseFile(line_generator, {'username':'darkid'}, fullName)
	except Exception as e:
		print 'Failed for file %s on line %d:' % (file, lineNo)
		with open(fullName, 'rb') as f:
			print f.read().split('\n')[lineNo]
		raise
