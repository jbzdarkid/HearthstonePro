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

rootDir = __file__.rpartition(sep)[0]
if rootDir == '':
    rootDir = '.'
rootDir += sep + 'tests'
    
if len(argv) == 1 or argv[1] == 'all':
    from os import listdir
    files = [rootDir+sep+file for file in listdir(rootDir)]
else: # pragma: no cover
    files = [rootDir+sep+file for file in argv[1:]]

config = {'username':'darkid'}
for file in files:
    try:
        Parser.parseFile(line_generator, {'username':'darkid'}, file)
    except Exception as e: # pragma: no cover
        logging.error('Failed for file %s on line %d:' % (file, lineNo))
        with open(file, 'rb') as f:
            line = f.read().split('\n')[lineNo]
            logging.error(line)
        raise
logging.info('Passed all tests!')
