import os


def init_colors() -> dict[str, str]:
    esc = '\x1B'
    reset = esc + '[0m'
    clear = esc + '[2J' + esc + '[H'
    bold = esc + '[1m'
    path_col = bold + esc + '[38;5;0m' + esc + '[48;5;255m'
    file_col1 = bold + esc + '[38;5;5m'
    file_col2 = bold + esc + '[48;5;5m' + esc + '[38;5;0m'
    folder_col1 = bold + esc + '[38;5;2m'
    folder_col2 = bold + esc + '[48;5;2m' + esc + '[38;5;0m'
    
    return {"esc": esc, "clear": clear, "bold": bold, "path_col": path_col, "reset": reset, "file_col1": file_col1,
            "file_col2": file_col2, "folder_col1": folder_col1, "folder_col2": folder_col2}


class Menu:
    def init(input_dir: str, prompt: str) -> str:
        curr_dir, colors, choice = input_dir, init_colors(), ''
        
        while choice not in ['Exit', 'exit']:
            dir_entries = Menu.print_dir(curr_dir, colors)
            files, folders = dir_entries[0], dir_entries[1]
            
            choice = input(
                f'\n{colors["bold"]}Use {colors["folder_col1"]}"go [folderName]"{colors["reset"]}{colors["bold"]} to switch folders, and {colors["file_col1"]}"select [filename]"{colors["reset"]}{colors["bold"]} to select a file. Enter "exit" to exit.\n{colors["file_col1"]}{prompt}')
            commands = choice.split(" ", maxsplit=1)
            
            if choice in ['Exit', 'exit']:
                break
            
            elif (commands[0] == 'go') and (commands[1] in folders) and (
              Menu.check_dir(f'{curr_dir}/{commands[1]}', colors)):
                if curr_dir == '/':
                    curr_dir = f'{curr_dir}{commands[1]}'
                else:
                    curr_dir = f'{curr_dir}/{commands[1]}'
            
            elif commands[0] == 'go':
                curr_dir = Menu.switch_dir(curr_dir, commands[1])
            
            elif commands[0] in files:  # This is for if the user selects file improperly.
                print(
                    f'This is a file, not a directory; directories are highlighted in {colors["folder_col1"]} green {colors["reset"]}.\n{colors["bold"]}To select a file, remember to use the "select" keyword and then the name of the file.\n')
            
            elif commands[0] == 'select' and commands[1] in files:
                print(colors["reset"], end='')
                return curr_dir + '/' + commands[1]
            
            elif commands[0] not in ['Exit', 'exit']:
                print(f'Not a valid option.')
    
    def switch_dir(old_dir: str, new_dir: str) -> str:
        dirs = new_dir.split('/')
        temp_dir = old_dir.split('/')
        file_count, dot_count, dir_add = 0, 0, []
        
        for i in range(len(dirs) - 1, -1, -1):  # Parses directory inputted.
            if (dirs[i] == '..') and (('..' in new_dir) or (
              '../' in new_dir)):  # Counts '..' instances for removing files from the current directory later
                dot_count += 1
            
            elif dirs[i] == '':  # Have to remove '' characters to prevent FileNotFound error
                dirs.remove(dirs[i])
            
            else:  # Counts # of directories inputted to append to 'currentDir'
                file_count += 1
                dir_add.append(dirs[i])
        
        if '..' in new_dir or '../' in new_dir:
            for i in range(0,
                           dot_count):  # Removes folders from 'new_dir' based off of 'dot_count' for rebuilding 'currentDir'
                temp_dir.remove(temp_dir[len(temp_dir) - 1])
        
        if file_count >= 1:  # Appends any folders inputted, if any
            for folder in dir_add:  # Appends new folders to 'new_dir' based off of 'file_count'
                temp_dir.append(folder)
        
        new_dir = ''
        for i in range(1, len(temp_dir)):
            new_dir += f'/{temp_dir[i]}'
        
        if new_dir == '':  # This allows for user to use '..' to go up to '/' directory.
            new_dir = '/'
        
        if Menu.check_dir(new_dir, init_colors()):
            return new_dir
        else:
            return old_dir
    
    def check_dir(input_dir: str,
                  colors: dict[
                      str, str]) -> bool:  # Checks if directory exists and is accessible, and prints out error message if not.
        try:
            os.scandir(input_dir)
        
        except (FileNotFoundError, NotADirectoryError):
            print(f'{colors["clear"]}Not a valid directory.')
            return False
        
        except PermissionError:
            print(f'{colors["clear"]}Directory not accessible; permission denied.')
            return False
        
        return True
    
    def print_dir(input_dir: str, colors: dict[str, str]) -> list:  # Prints all files and folders in directory
        files, folders, file_count, folder_count = [], [], 0, 0
        
        if Menu.check_dir(input_dir, colors):
            curr_dir = os.scandir(input_dir)
            for entry in curr_dir:
                if entry.is_file():  # Need to keep lists separate for sorted output and commands
                    files.append(entry.name)
                elif entry.is_dir():
                    folders.append(entry.name)
            
            print(f'{colors["reset"]}[*] {colors["path_col"]}{input_dir}{colors["reset"]}')
            if len(folders) == 0 and len(files) == 0:
                print(fr'{colors["bold"]} \-> No content in this directory')
            
            else:
                for i in range(0, len(folders)):
                    if i % 2 == 0:
                        print(fr'{colors["folder_col1"]} \-> {folders[i]}{colors["reset"]}')
                    else:
                        print(fr' {colors["folder_col2"]}\-> {folders[i]}{colors["reset"]}')
                for i in range(0, len(files)):
                    if i % 2 == 0:
                        print(fr'{colors["file_col1"]} \-> {files[i]}{colors["reset"]}')
                    else:
                        print(fr' {colors["file_col2"]}\-> {files[i]}{colors["reset"]}')
        
        return [files, folders]
