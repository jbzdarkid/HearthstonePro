from sys import argv
import Parser

def line_generator(file):
	f = open(file, 'rb')
	for line in f:
		yield line

if len(argv) == 1 or argv[1] == 'all':
	from os import listdir
	files = listdir('tests')
# elif argv[1] == 'latest':
#   from os.path import getmtime
else:
	files = argv[1:]

config = {'username':'darkid'}
for file in files:
	try:
		Parser.parseFile(line_generator, {'username':'darkid'})
	except Exception as e:
		from traceback import print_exc
		print 'Failed for file', file
		print_exc()
