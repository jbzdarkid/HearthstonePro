import logging
from sys import argv
from os import sep
import Parser

# logging.getLogger().setLevel(logging.DEBUG)
assert Parser.parse('') == {}
assert Parser.parse('a=b') == {'a':'b'}
assert Parser.parse('a=b c') == {'a':'b c'}
assert Parser.parse('a=[b=c]') == {'a':{'b':'c'}}
assert Parser.parse('a=b c=d') == {'a':'b', 'c':'d'}
assert Parser.parse('a=[b=c d]') == {'a':{'b':'c d'}}
assert Parser.parse('a=[b=c] d=e') == {'a':{'b':'c'}, 'd':'e'}
assert Parser.parse('a=[b=c d=e]') == {'a':{'b':'c', 'd':'e'}}
assert Parser.parse('a=b c d=e') == {'a':'b c', 'd':'e'}
assert Parser.parse('a=b c=[d=e] f=g') == {'a':'b', 'c':{'d':'e'}, 'f':'g'}
assert Parser.parse('a=[b=c d=e] f=g') == {'a':{'b':'c', 'd':'e'}, 'f':'g'}
assert Parser.parse('a[b]=c') == {'a[b]':'c'}
assert Parser.parse('a[b]=c d') == {'a[b]':'c d'}
assert Parser.parse('a[b]=c d=e') == {'a[b]':'c', 'd':'e'}
assert Parser.parse('a[b]=c d e=f') == {'a[b]':'c d', 'e':'f'}
assert Parser.parse('a[b]=c d=[e=f]') == {'a[b]':'c', 'd':{'e':'f'}}
assert Parser.parse('a[b]=c d=e f[g]=h') == {'a[b]':'c', 'd':'e', 'f[g]':'h'}

def line_generator(file):
    global lineNo
    lineNo = 0
    f = open(file, 'rb')
    for line in f:
        yield line
        lineNo += 1

rootDir = __file__.rsplit(sep)[0]

if len(argv) == 1 or argv[1] == 'all':
    from os import listdir
    files = ['tests'+sep+file for file in listdir(rootDir+sep+'tests')]
# elif argv[1] == 'latest': # pragma: no cover
#   from os.path import getmtime
else: # pragma: no cover
    files = argv[1:]

logging.critical('\nrootDir: ' + str(rootDir))
logging.critical('\nfiles: ' + str(files))
logging.critical('\nfiles[0]: ' + str(files[0]))
logging.critical('\nfullName: ' + str(rootDir+sep+files[0]))

config = {'username':'darkid'}
for file in files:
    fullName = rootDir+sep+file
    logging.critical(fullName)
    try:
        Parser.parseFile(line_generator, {'username':'darkid'}, fullName)
    except Exception as e: # pragma: no cover
        logging.error('Failed for file %s on line %d:' % (file, lineNo))
        with open(fullName, 'rb') as f:
            line = f.read().split('\n')[lineNo]
            logging.error(line)
        raise
logging.info('Passed all tests!')
