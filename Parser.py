# Displaying with tk:
# Use Toplevel() in construction, and root.lift() as a backup

import logging
# CRITICAL: Unused
# ERROR: Errors (duh)
# WARNING: Minimal logging; Game start/end and hand at start of turn
# INFO: Heavy logging; all events -- still reads like english
# DEBUG: Full logging; all partial states (Warning: slow) -- code jargon everywhere
# 5: Stupid levels of printout (basically only for the parser)
logging.basicConfig(format='%(message)s', level=logging.INFO)

import Cards, Hand, Legendaries, Utilities, Dragons
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
    key = None
    while i < len(data):
        if data[i] == '[':
            logging.log(5, 'Recursing...')
            ret = parse(data, i+1)
            if isinstance(ret, tuple):
                logging.log(5, 'Recursion returned: ' + str(ret))
                out[key], i = ret
                possible = start
                recursed = True
            else:
                logging.log(5, 'Recursion returned a signal, continuing key')
                i = ret
        elif data[i] == ']':
            if key is None:
                logging.log(5, 'No key found during recursion')
                return i
            logging.log(5, '<1>Value: data[%d:%d]=%s' % \
                (index, i, data[index:i]))
            value = data[index:i]
            out[key] = value
            return (out, i)
        elif data[i] == ' ':
            logging.log(5, 'Possible value: data[%d:%d]=%s' % \
                (index, i, data[index:i]))
            possible = i+1
        elif data[i] == '=':
            if not recursed:
                logging.log(5, '<2>Value: data[%d:%d]=%s' % \
                    (index, possible-1, data[index:possible-1]))
                out[key] = data[index:possible-1]
            logging.log(5, 'Key: data[%d:%d]=%s' % \
                (possible, i, data[possible:i]))
            key = data[possible:i]
            index = i+1
            recursed = False
        i += 1
    if not recursed: # The last k,v pair
        out[key] = data[index:]
        logging.log(5, '<3>Value: data[%d:]=%s' % (index, out[key]))
    logging.debug('Finished parsing, result:' + str(out))
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
        line_parts = match(b'^D \d{2}:\d{2}:\d{2}\.\d{7} ([a-zA-Z]*\.[a-zA-Z]*\(\)) -\s*([A-Z_]{2,}|)(.*)', line)
        if line_parts is None: # Any of the error messages won't match, but it's not safe to use them
            continue
        source = line_parts.group(1)
        type = line_parts.group(2)
        data = parse(line_parts.group(3))

        if source == 'GameState.DebugPrintEntityChoices()':
            if 'ChoiceType' in data and data['ChoiceType'] == 'MULLIGAN':
                if data['Player'].decode('utf-8') == config['username']:
                    logging.debug('You are player id %s' % data['id'])
                    Utilities.us = data['id']
                else:
                    logging.debug('Opponent is player id %s' % data['id'])
                    Utilities.them = data['id']
        if source == 'GameState.DebugPrintEntitiesChosen()':
            # Cards that were not mulliganed
            if data.keys()[0][:8] == 'Entities': # Entities[0], e.g.
                if data.values()[0]['zone'] == 'HAND':
                    Hand.keep(data.values()[0])
        if source == 'PowerTaskList.DebugPrintPower()':
            if type == 'BLOCK_END':
                Cards.blockEnd()
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
                        Legendaries.play3(data['Entity'], data['Target'])
                        Dragons.play3(data['Entity'], data['Target'])
                    else:
                        Cards.play2(data['Entity'])
                        Legendaries.play2(data['Entity'])
                        Dragons.play2(data['Entity'])
            elif type == 'FULL_ENTITY':
                data = data[None] # Always starts with 'Updating'
                if data['zone'] == 'HAND':
                    # A backup for Princess Huhuran. All that is revealed in the log
                    # is the target, but this line always appears when a card is drawn.
                    Hand.draw(position=int(data['zonePos'])-1)
            elif type == 'SHOW_ENTITY': # Start of a SHOW_ENTITY block of data
                Cards.showentity(data)
            elif type == 'TAG_CHANGE':
                if data['tag'] == 'FIRST_PLAYER':
                    logging.warning('New game started')
                    Utilities.wentFirst(data['Entity'] == config['username'])
                elif data['tag'] == 'JUST_PLAYED':
                    if data['Entity']['zone'] == 'HAND':
                        Dragons.play(data['Entity']) # List before Hand.play
                        Hand.play(data['Entity']) # When a card is removed from a player's hand
                elif data['tag'] == 'NUM_TURNS_IN_PLAY':
                    # A number of things, including which player has which hero.
                    Utilities.set_hero(data['Entity'])
                elif data['tag'] == 'RESOURCES':
                    if data['Entity'] != config['username']:
                        Utilities.resources = data['value']
                elif data['tag'] == 'STEP':
                    if data['value'] == 'FINAL_GAMEOVER':
                        Hand.reset()
                        Utilities.reset()
                        Legendaries.reset()
                        Dragons.reset()
                        logging.warning('Game Over')
                    if data['value'] == 'MAIN_READY':
                        if Utilities.ourTurn():
                            Hand.turnover()
                            Cards.turnover()
                            Legendaries.turnover()
                            Dragons.turnover()
                        else:
                            logging.info('End of your turn')
                elif data['tag'] == 'TURN':
                    Utilities.turn = int(data['value'])
                elif data['tag'] == 'ZONE':
                    print data
                    if 'value' == 'REMOVEDFROMGAME':
                        Cards.removed_from_game(data['Entity'])
                elif data['tag'] == 'ZONE_POSITION':
                    if 'zone' in data['Entity'] and data['Entity']['zone'] == 'DECK':
                        Hand.draw(data['Entity'], int(data['value'])-1)
                elif data['tag'] == 'ZONE':
                    if 'zone' in data['Entity']:
                        if data['value'] == 'PLAY':
                            Dragons.setaside(data['Entity'])
                        if data['value'] == 'REMOVEDFROMGAME':
                            Cards.die2(data['Entity']) # Enchantment death

# Setup scripts.
if __name__ == '__main__': # pragma: no cover
    from json import load, dump
    from os import sep, walk
    from os.path import expanduser, exists
    from platform import system
    from re import search
    from time import sleep
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
        logging.warning('Config incomplete or corrupted, (re)generating.')
        logging.warning('This might take a while...')

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
                        f = open(root+sep+files[0]).read()
                        # FIXME don't need to re-open f?
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

    # FIXME why am I checking contents if I overwrite anyways
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

    logging.warning('Startup complete.')

    def tail():
        try: # Create the file if it doesn't exist
            open(config['log']+'Power.log', 'w')
        except:
            pass
        if not exists(config['log']+'Power.log'):
            logging.error('Please (re)start Hearthstone before running this script.')
            exit(-1)
        with open(config['log']+'Power.log') as f:
            f.seek(0, 2) # Go to EOF
            while True:
                lastLine = f.readline()
                if not lastLine:
                    sleep(0.01)
                    continue
                yield lastLine

    parseFile(tail, config)
