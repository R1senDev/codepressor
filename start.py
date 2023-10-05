title = 'Codepressor   by R1senDev'

import os
import re
import sys
import shutil

import time

try:
    from colorama import init
except:
    input('[!] Please, wait; there is something to install before the first launch. Press [Enter] to continue.\n')
    os.system('pip install colorama')
    try:
        from colorama import init
    except:
        print('\n\n"Something" does not want to be installed. Please install the following libraries manually:\n- colorama\n\nPress [Ctrl]+[C] to exit.\n')
        while True:
            pass
init()
from colorama import Fore, Style

sw = int(str(shutil.get_terminal_size()).split('=')[1].split(',')[0])
print(f'{Style.BRIGHT}\n{title.center(sw)}{Style.RESET_ALL}')

def argIsProvided(arg):
    for a in sys.argv:
        if a == arg:
            return True
    return False

def getArgPos(arg):
    for aPos in range(1, len(sys.argv)):
        if sys.argv[aPos] == arg:
            return aPos
    return -1

def getArgValue(arg, default=''):
    if argIsProvided(arg):
        if len(sys.argv) >= getArgPos(arg) + 1:
            return sys.argv[getArgPos(arg) + 1]
        else:
            return default
    else:
        return default

templates = [
    ['\t', ''],

    [' {', '{'],
    ['{ ', '{'],
    [' }', '}'],
    ['} ', '}'],
    [' [', '['],
    ['[ ', '['],
    [' ]', ']'],
    ['] ', ']'],
    [' (', '('],
    ['( ', '('],
    [' )', ')'],
    [') ', ')'],

    [' =', '='],
    ['= ', '='],
    [' <', '<'],
    ['< ', '<'],
    [' >', '>'],
    ['> ', '>'],
    [' +', '+'],
    ['+ ', '+'],
    [' -', '-'],
    ['- ', '-'],
    [' *', '*'],
    ['* ', '*'],
    [' /', '/'],
    ['/ ', '/'],
    [' %', '%'],
    ['% ', '%'],
    [' ,', ','],
    [', ', ','],
    [' :', ':'],
    [': ', ':'],
    [' !', '!'],
    ['! ', '!'],

    ['case \'', 'case\''],

    [' &', '&'],
    ['& ', '&'],
    [' |', '|'],
    ['| ', '|'],

    ['function*', 'function* '],
]

fixes = [
    [';)', ')'],
    ['(;', '('],
    [';]', ']'],
    ['[;', '['],
    [';}', '}'],
    ['{;', '{'],

    [',]', ']'],
    [', ]', ']'],
    [',}', '}'],
    [', }', '}'],
    [',;', ','],
    [':;', ':'],

    ['; ', ';'],
]

if argIsProvided('-h') or argIsProvided('--help') or len(sys.argv) == 1:
    print(f'\nUsage: start.py sourceFile [destinationFile] [args]\n\nOptional arguments:\n{"-h, --help".center(20)}  Shows this message.\n{"-s".center(20)}  Disables logging.\n{"--ignore-newlines".center(20)}  Ignores newline characters. Significantly reduces the compression efficiency.\n')
elif len(sys.argv) > 2:
    if sys.argv[1] == sys.argv[2]:
        overwrite = input(f'The source file and the destination file are the same. Are you sure you want to {Fore.RED}overwrite the source file{Style.RESET_ALL}?\n[B]ackup and overwrite/[O]verwrite/[A]bort: ')
        if overwrite.lower() == 'b':
            shutil.copyfile(sys.argv[1], f'{sys.argv[1]}.bkp')
        elif overwrite.lower() == 'o':
            print(f'\n{Fore.RED}I hope you thought before doing this.{Style.RESET_ALL}')
        else:
            print('\nAbort.')
            exit
    print(f'\n{"Processing... ".center(sw)}')
    oldSize = os.path.getsize(sys.argv[1])
    logging = not argIsProvided('-s')

    if not re.findall(r'\.py.?', sys.argv[1]):
        with open(sys.argv[1], 'r') as sf:
            data = sf.read()

        lens = [len(data), 0]

        while '  ' in data:
            data = data.replace('  ', ' ')
        lens[1] = len(data)
        if lens[0] - lens[1] > 0 and logging:
                with open('log.txt', 'a') as log:
                    log.write(f'\n\nDoubleWhitespaces: removed {lens[0] - lens[1]} symbols\n')

        lens[0] = len(data)
        data = re.sub(r'\/\/.*', '', data)
        lens[1] = len(data)
        if lens[0] - lens[1] > 0 and logging:
            with open('log.txt', 'a') as log:
                log.write(f'Comments: removed {lens[0] - lens[1]} symbols\n')

        lens[0] = len(data)
        for pair in templates:
            data = data.replace(pair[0], pair[1])
        lens[1] = len(data)
        if lens[0] - lens[1] > 0 and logging:
            with open('log.txt', 'a') as log:
                log.write(f'Templates: removed {lens[0] - lens[1]} symbols\n')

        if not argIsProvided('--ignore-newlines'):
            lens[0] = len(data)
            data = data.replace('\n', ';')
            while ';;' in data:
                data = data.replace(';;', ';')
            lens[1] = len(data)
            if lens[0] - lens[1] > 0 and logging:
                with open('log.txt', 'a') as log:
                    log.write(f'Newlines: removed {lens[0] - lens[1]} symbols\n')

        lens[0] = len(data)
        for pair in fixes:
            data = data.replace(pair[0], pair[1])
        lens[1] = len(data)
        if lens[0] - lens[1] > 0 and logging:
            with open('log.txt', 'a') as log:
                log.write(f'PostProcessing: removed {lens[0] - lens[1]} symbols\n\n\n')

        with open(sys.argv[2], 'w') as dest:
            dest.write(data)
        print(Fore.GREEN + f'Done{Style.RESET_ALL}'.center(sw) + Style.RESET_ALL)
        oldSizeVal = 'B'
        dmem = abs(oldSize - os.path.getsize(sys.argv[2]))
        if oldSize >= 1024:
            oldSize = round(oldSize / 1024, 2)
            oldSizeVal = 'kB'
        newSize = os.path.getsize(sys.argv[2])
        newSizeVal = 'B'
        if newSize >= 1024:
            newSize = round(newSize / 1024, 2)
            newSizeVal = 'kB'
        fsdstr = Fore.RED + str(oldSize) + f'{oldSizeVal}{Style.RESET_ALL} -> ' + Fore.GREEN + str(newSize) + newSizeVal + Style.RESET_ALL
        dmemVal = 'B'
        if dmem >= 1024:
            dmem = round(dmem / 1024, 2)
            dmemVal = 'kB'
        print(f'\nFile size:\n{fsdstr}\n\n{Fore.GREEN}{str(dmem).split(".")[0]}.{str(dmem).split(".")[1][:2]}{dmemVal}{Style.RESET_ALL} freed!\n')
    else:
        print('Python code is not supported yet.\n\nDo you want to help? Fork the project (https://github.com/R1senDev/codepressor), modify it and create a Pull Request! :)')
