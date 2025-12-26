# This script is only intended to demo the functionality of the file picker module, and DOES NOT have to be used in conjunction with it.

from os import getcwd, scandir
from pypicker import Menu as Picker

start, current_dir = False, getcwd()
print('\x1B' + '[2J' + '\x1B' + '[H' + '\x1B' + '[0m', end='')  # Resets any terminal formatting and moves cursor back to home position

while not start:  # Menu loop for testing function
    current_dir = input('\x1B' + '[1m' + 'Enter path, or press ENTER to use CWD: ')
    if current_dir == '':
        current_dir = getcwd()

    elif current_dir != '/' and current_dir.endswith('/'):  # Removes "/" suffix to prevent issues with manipulating directory string
        current_dir = current_dir.removesuffix('/')
    

    try:  # Checks if directory is valid, and starts pyPicker if true.
        scandir(current_dir)
        start = True
    
    except PermissionError:
        print('\nDirectory not accessible; permission denied.')
    
    except(FileNotFoundError, NotADirectoryError):
        print('\nNot a valid directory.')

print(Picker.init(current_dir, '[>>>] Select a file: '))
