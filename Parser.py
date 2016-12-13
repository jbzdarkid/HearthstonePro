# Displaying with tk:
# Use Toplevel() in construction, and root.lift() as a backup

import logging
# CRITICAL: No logging (errors only)
# ERROR: Unused
# WARNING: Minimal logging; Game start/end and hand at start of turn
# INFO: Heavy logging; all events -- still reads like english
# DEBUG: Full logging; all partial states (Warning: slow) -- code jargon everywhere
logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format='%(message)s')

import Cards, Dragons, Hand, Legendaries, Utilities
def parse(data, start=0, DEBUG=False):
    '''
    This function parses a hearthstone line and returns
    a dictionary.
    Python throws some warnings here about
    'key may not be defined', but an error will only be
    thrown on improperly formatted input.
    '''
    data = data.strip()
    out = {}
    index = start
    possible = start
    i = start
    recursed = True
    while i < len(data):
        logging.debug(i, data[i])
        if data[i] == '[' and data[i-1] == '=':
            logging.debug('Recursing...')
            out[key], i = parse(data, i+1)
            possible = start
            recursed = True
            logging.debug('Recursion returned:', out[key])
        elif data[i] == ']':
            if not recursed:
                value = data[index:i]
                logging.debug('<1>Value: data[%d:%d]=%s', (index, i, value))
                out[key] = value
                return (out, i)
        elif data[i] == ' ':
            possible = i+1
            logging.debug('Possible value: data[%d:%d]=%s',
                (index, possible-1, data[index:possible-1]))
        elif data[i] == '=':
            if not recursed:
                out[key] = data[index:possible-1]
                logging.debug('<2>Value: data[%d:%d]=%s',
                    (index, possible-1, out[key]))
            key = data[possible:i]
            logging.debug('Key: data[%d:%d]=%s', (possible, i, key))
            index = i+1
            recursed = False
        i += 1
    if not recursed: # The last k,v pair
        out[key] = data[index:]
        logging.debug('<3>Value: data[%d:]=%s', (index, out[key]))
    logging.debug('Finished parsing, result:' +str(out))
    return out

def parseFile(line_generator, config, *args):
    '''
    Main parsing function.
    line_generator can be a tail for live execution,
    or a file object for testing.
    '''
    lineNo = 0
    from re import match
    showEntity = None
    for line in line_generator(*args):
        lineNo += 1
        line_parts = match('^D \d{2}:\d{2}:\d{2}\.\d{7} ([a-zA-Z]*\.[a-zA-Z]*\(\)) -\s*([A-Z_]{2,}|)(.*)', line)
        if line_parts is None: # Any of the error messages won't match, but it's not safe to use them
            continue
        source = line_parts.group(1)
        type = line_parts.group(2)
        data = parse(line_parts.group(3))

        if source == 'GameState.DebugPrintPower()' and type =='TAG_CHANGE':
            if data['tag'] == 'PLAYER_ID':
                if data['Entity'] == config['username']:
                    Utilities.us = data['value']
                else:
                    Utilities.them = data['value']
            elif data['tag'] == 'FIRST_PLAYER':
                Utilities.wentFirst(data['Entity'] == config['username'])
        if source == 'GameState.DebugPrintEntitiesChosen()':
            # Cards that were not mulliganed
            if data.keys()[0][:8] == 'Entities': # Entities[0], e.g.
                if data.values()[0]['zone'] == 'HAND':
                    Hand.keep(data.values()[0])
        if showEntity is not None:
            if type:
                showEntity = None
            elif 'tag' in data and data['tag'] == 'ZONE' and data['value'] == 'GRAVEYARD':
                Hand.discard(showEntity)
        if source == 'PowerTaskList.DebugPrintPower()':
            if type == 'BLOCK_END':
                Legendaries.blockEnd()
            elif type == 'BLOCK_START':
                if data['BlockType'] == 'TRIGGER':
                    if 'zone' in data['Entity']:
                        if data['Entity']['zone'] == 'GRAVEYARD':
                            Cards.die(data['Entity'])
                            Legendaries.die(data['Entity'])
                            Dragons.die(data['Entity'])
                        elif data['Entity']['zone'] == 'PLAY':
                            Cards.trigger(data['Entity'])
                elif data['BlockType'] == 'POWER': # When a card actually hits the board
                    if 'Target' in data and isinstance(data['Target'], dict):
                        Cards.play3(data['Entity'], data['Target']) # A card targets another card.
                        Dragons.play3(data['Entity'], data['Target'])
                        Legendaries.play3(data['Entity'], data['Target'])
                    else:
                        Cards.play2(data['Entity'])
                        Dragons.play2(data['Entity'])
                        Legendaries.play2(data['Entity'])
            elif type == 'SHOW_ENTITY': # Start of a SHOW_ENTITY block of data
                showEntity = data['Entity']
            elif type == 'TAG_CHANGE':
                if data['tag'] == 'JUST_PLAYED':
                    if data['Entity']['zone'] == 'HAND':
                        Hand.play(data['Entity']) # When a card is removed from a player's hand
                elif data['tag'] == 'NUM_TURNS_IN_PLAY':
                    if data['value'] == '1':
                        Dragons.play4(data['Entity'])
                elif data['tag'] == 'RESOURCES':
                    if data['Entity'] != config['username']:
                        Utilities.resources = data['value']
                elif data['tag'] == 'STEP':
                    if data['value'] == 'FINAL_GAMEOVER':
                        Hand.reset()
                        Utilities.reset()
                        Legendaries.reset()
                        print 'Game Over'
                elif data['tag'] == 'TURN':
                    Utilities.turn = int(data['value'])
                    # TODO: Delay going first until after mulligan resolves, since the mulligan labels are wrong
                    if (int(data['value']) + Utilities.turnOffset)%2 == 0:
                        Cards.turnover()
                        Hand.turnover()
                        Legendaries.turnover()
                elif data['tag'] == 'ZONE_POSITION':
                    if 'zone' in data['Entity'] and data['Entity']['zone'] == 'DECK':
                        Hand.draw(data['Entity'], int(data['value'])-1)

# Setup scripts.
if __name__ == '__main__': # pragma: no cover
    from json import load, dump
    from os import sep
    from os.path import expanduser, exists
    from subprocess import PIPE
    rootDir = __file__.rpartition(sep)[0]
    # If rootDir is nothing, then ''+'/' = '/', which is not the current directory.
    if rootDir:
        rootDir += sep

    try:
        config = load(open(rootDir+'config.cfg'))
    except IOError:
        # Config not defined, somehow. Recreate.
        config = {}
    except (SyntaxError, ValueError):
        # Config corrupt, somehow. Recreate.
        config = {}

    if any(key not in config for key in ['logconfig', 'log', 'username']):
        print 'Config incomplete or corrupted, (re)generating. This might take a while...'
        from platform import system
        from os import walk
        if system() == 'Windows':
            config['logconfig'] = expanduser('~')+'\AppData\Local'
            appName = 'Hearthstone.exe'
        elif system() == 'Darwin': # Mac OSX
            config['logconfig'] = expanduser('~')+'/Library/Preferences'
            appName = 'Hearthstone.app'
        else:
            raise Exception('Unknown platform:', system())
        config['logconfig'] += '/Blizzard/Hearthstone/log.config'

        for root, dirs, files in walk(expanduser('~')):
            if root.rsplit(sep)[-1] == 'Logs':
                for f in files:
                    if 'battle.net' in f:
                        from re import search
                        f = open(root+sep+files[0]).read()
                        m = search('m_battleTag: (.*?)#', f)
                        config['username'] = m.group(1)
                        break
            if appName in dirs+files:
                config['log'] = root + sep + 'Logs' + sep
            if 'username' in config and 'log' in config:
                break
    if 'log' not in config:
        config['log'] = raw_input('Please locate your Hearthstone.exe install:').rpartition(sep)[0]+sep+'Logs'+sep
    if 'username' not in config:
        config['username'] = raw_input('Please input your battle.net name, without the #1234:')

    with open(rootDir+'config.cfg', 'wb') as f:
        dump(config, f)

    f = open(rootDir+'log.config', 'rb').read()
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

    print 'Startup complete.'

    def tail():
        from time import sleep
        try: # Create the file if it doesn't exist
            open(config['log']+'Power.log', 'w')
        except:
            pass
        if not exists(config['log']+'Power.log'):
            print 'Please (re)start Hearthstone before running this script.'
            exit(-1)
        with open(config['log']+'Power.log') as f:
            f.seek(0, 2)
            while True:
                lastLine = f.readline()
                if not lastLine:
                    sleep(0.01)
                    continue
                yield lastLine

    parseFile(tail, config)
