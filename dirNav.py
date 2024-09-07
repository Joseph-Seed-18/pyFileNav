import os

esc = '\x1B'
bold = esc + '[1m'
path = bold + esc + '[38;5;0m' +esc + '[48;5;255m'
reset = esc + '[0m'
fileCol1 = bold + esc + '[38;5;5m'
fileCol2 = bold + esc + '[48;5;5m' + esc + '[38;5;0m'
folderCol1 = bold + esc + '[38;5;2m'
folderCol2 = bold + esc + '[48;5;2m' + esc + '[38;5;0m'
clear = esc + '[2J' + esc + '[H'

start = False
print(clear + reset, end='')

while (not(start)):
    currentDir = input(f'{bold}Enter path, or press ENTER to use CWD: ')
    if currentDir == '':
        currentDir = os.getcwd()
    elif currentDir.endswith('/'):
        currentDir = currentDir.removesuffix('/')

    try:
        dirScan = os.scandir(currentDir)
        start = True
        dirScan.close()
    except(PermissionError):
        print('\nDirectory not accessible; permission denied.')
    except(FileNotFoundError):
        print('\nNot a valid directory.')


def dirNav(currentDir, prompt):
    choice, error = '', ''
    loopCount = 0
    while(choice != 'exit'):

        if error != '':
                print(f'{clear}{error}\n[*] {path}{currentDir}{reset}')
                error = ''
        else:
            print(f'{clear}[*] {path}{currentDir}{reset}')

        try:
            with os.scandir(currentDir) as dirScan: #Short for 'directory entry'
                files, folders = [], []

                for entry in dirScan: #Takes entries from directory scanner and puts into list
                    if(entry.is_file()): #Need to keep lists separate for sorted output and commands
                        files.append(entry.name)
                    elif(entry.is_dir()):
                        folders.append(entry.name)

                if len(folders) == 0 and len(files) == 0 :
                    print(fr'{bold} \-> No content in this directory')
                else:
                    for i in range(0, len(folders)):
                        if i % 2 == 0:
                            print(fr'{folderCol1} \-> {folders[i]}{reset}')
                        else:
                            print(fr' {folderCol2}\-> {folders[i]}{reset}')

                    for i in range(0, len(files)):
                        if i % 2 == 0:
                            print(fr'{fileCol1} \-> {files[i]}{reset}')
                        else:
                            print(fr' {fileCol2}\-> {fileCol2}{files[i]}{reset}')

        except(PermissionError):
            error = 'Directory not accessible; permission denied.'
            print(f'{clear}{bold}{error}\n[*] {path}{currentDir}{reset}')
            error = ''

        choice = input(f'\n{bold}{prompt}')
        commands = choice.split(" ")
        
        if choice in ['exit', 'Exit']:
            break


        elif (commands[0] == 'go') and (commands[1] in folders):
            currentDir = f'{currentDir}/{commands[1]}'

        
        elif (commands[0] == 'go'):
            #dirs = commands[1].split('/') #Returns all directories and '..' instances from 'commands[1]' in ordered list
            dirs, fileCount, dirAdd, newDir, tempDir = (commands[1].split('/')), 0, [], (currentDir.split('/')), ''
            #newDir = currentDir.split('/') #Returns list of folders in current path, which will be rebuilt with 'dirs'

            if ('..' in commands[1]) or ('../' in commands[1]):
                dotCount = 0


            for i in range(0, len(dirs)):
                if (('..' in commands[1]) or ('../' in commands[1])) and (dirs[i] == '..'): #Counts '..' instances for removing files from 'currentDir'
                    dotCount += 1
                elif dirs[i] == '': #Have to remove '' characters to prevent FileNotFound error
                    dirs.remove(dirs[i])
                    i -= 1 #Dangerous yes, but needed to remain in list bounds
                else: #Counts directories inputted to append to 'currentDir'
                    fileCount += 1
                    dirAdd.append(dirs[i])


            if ('..' in commands[1]) or ('../' in commands[1]):
                for i in range(0, dotCount): #Removes folders from 'newDir' based off of 'dotCount' for rebuilding 'currentDir'
                    newDir.remove(newDir[len(newDir) - 1])

            if(fileCount >= 1): #Appends any folders inputted, if any
                for i in range(0, len(dirAdd)): #Appends new folders to 'newDir' based off of 'fileCount' 
                    newDir.append(dirAdd[i])

            try: #Catches FileNotFound error
                for i in range(1, len(newDir)): #Rebuilds path string with removed directories
                    tempDir += f'/{newDir[i]}'
                dirScan = os.scandir(tempDir)
                dirScan.close()
            
            except (FileNotFoundError):
                error = 'Directory does not exist.'

            except(PermissionError):
                error = 'Directory not accessible; permission denied.'

            if error == '':
                currentDir = tempDir


        elif commands[1] in files: #This for if user mistakes file for directory, or attempts to select file improperly
            print('You have selected a file, not a directory. To select a file, type "select", and the name of the file.')

        
        elif commands[0] not in ['exit', 'Exit']:
            print(f'Not a valid option.')

        loopCount += 1
print(dirNav(currentDir, 'Enter "go" and the name of folder to change directories, or use "select [filename]" to select a file: '))
