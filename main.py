import os

from dirNav import Menu as FilePicker

start, currentDir = False, os.getcwd()
print('\x1B' + '[2J' + '\x1B' + '[H' + '\x1B' + '[0m', end='')
while not start:  # Menu for testing function
    currentDir = input('\x1B' + '[1m' + 'Enter path, or press ENTER to use CWD: ')
    if currentDir == '':
        currentDir = os.getcwd()
    elif currentDir.endswith('/'):
        currentDir = currentDir.removesuffix('/')
    
    try:
        os.scandir(currentDir)
        start = True
    
    except PermissionError:
        print('\nDirectory not accessible; permission denied.')
    
    except(FileNotFoundError, NotADirectoryError):
        print('\nNot a valid directory.')
print(FilePicker.init(currentDir, '[>>>] Select a file: '))
