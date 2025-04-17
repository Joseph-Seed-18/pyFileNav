# This script is only intended to demo the functionality of the file picker module, and DOES NOT have to be used in conjunction with it.

import os

from fp import Menu as FP

start, currentDir = False, os.getcwd()
print('\x1B' + '[2J' + '\x1B' + '[H' + '\x1B' + '[0m',
      end='')  # Resets any terminal formatting and moves cursor back to home position

while not start:  # Menu for testing function
    currentDir = input('\x1B' + '[1m' + 'Enter path, or press ENTER to use CWD: ')
    if currentDir == '':  # Uses CWD if user hits enter
        currentDir = os.getcwd()
    
    elif currentDir != '/' and currentDir.endswith('/'):  # Removes '/' suffix to prevent issues
        currentDir = currentDir.removesuffix('/')
    
    try:  # Checks if directory is valid, and exits menu if so. Otherwise, prints special error messages
        os.scandir(currentDir)
        start = True
    
    except PermissionError:
        print('\nDirectory not accessible; permission denied.')
    
    except(FileNotFoundError, NotADirectoryError):
        print('\nNot a valid directory.')

print(FP.init(currentDir, '[>>>] Select a file: '))
