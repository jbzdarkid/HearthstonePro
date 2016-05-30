from sys import argv
from os import sep
import Parser

rootDir = __file__.rpartition(sep)[0]
# If rootDir is nothing, then ''+'/' = '/', which is not the current directory.
if rootDir: # pragma: no cover
    rootDir += sep

def line_generator(file):
    global lineNo
    lineNo = 0
    f = open(file, 'rb')
    for line in f:
        yield line
        lineNo += 1

if len(argv) == 1 or argv[1] == 'all':
    from os import listdir
    files = listdir(rootDir+'tests')
# elif argv[1] == 'latest': # pragma: no cover
#   from os.path import getmtime
else: # pragma: no cover
    files = argv[1:]

config = {'username':'darkid'}
for file in files:
    fullName = rootDir+'tests'+sep+file
    try:
        Parser.parseFile(line_generator, {'username':'darkid'}, fullName)
    except Exception as e: # pragma: no cover
        print 'Failed for file %s on line %d:' % (file, lineNo)
        with open(fullName, 'rb') as f:
            print f.read().split('\n')[lineNo]
        raise
