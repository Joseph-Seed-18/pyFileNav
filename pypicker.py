from os import scandir

@staticmethod
def init_colors() -> dict[str, str]:  # Returns a dict containing ANSI escape codes for formatting terminal output.
    # Any additional codes should be added in this function, and be referenced from the dict.

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


class Menu:  # Contains all functionality for pyPicker.
    
    @staticmethod
    def init(input_dir: str, prompt: str) -> str:
        curr_dir = input_dir
        colors = init_colors() # Dict of ANSI escape codes
        choice = '' # User input


        while choice not in ['Exit', 'exit']: # Menu loop for pyPicker interface

            if curr_dir.endswith("/"): # Removes extra "/" at end, for proper display of path
                curr_dir = curr_dir[0 : curr_dir.__sizeof__() - 1]


            dir_entries = Menu.get_dir_contents(curr_dir, colors)
            files, folders = dir_entries[0], dir_entries[1]
            
            choice = input(
                f'\n{colors["bold"]}Enter {colors["folder_col1"]}"go [folderName]"{colors["reset"]}{colors["bold"]} to switch folders, or {colors["file_col1"]}"select [filename]"{colors["reset"]}{colors["bold"]} to select a file. Enter "exit" to exit.\n{colors["file_col1"]}{prompt}')
            
            commands = choice.split(" ", maxsplit=1) # Splits keyword from directory
            

            if choice in ['Exit', 'exit']:
                return None
            

            elif (commands[0] == 'go') and (commands[1] in folders) and (Menu.check_dir(f'{curr_dir}/{commands[1]}', colors)): # If input contains more than 1 folder
                
                if curr_dir == '/':
                    curr_dir = f'{curr_dir}{commands[1]}'
                
                else:
                    curr_dir = f'{curr_dir}/{commands[1]}'
            
            elif commands[0] == 'go' and commands[1] in files:  # This prevents user from attempting to "go" to file instead of a folder.
                print(
                    f'This is a file, not a directory; directories are highlighted in {colors["folder_col1"]} green {colors["reset"]}.\n{colors["bold"]}To select a file, use the "select" keyword and then the name of the file.\n')
            
            elif commands[0] == 'go':
                curr_dir = Menu.switch_dir(curr_dir, commands[1])
            

            elif commands[0] == 'select' and commands[1] in folders: # This prevents user from "selecting" a folder instead of a file.
                # COMMENT / REMOVE THIS BLOCK OF CODE OUT IF SELECTION OF FOLDERS IS PERMITTED. 

                print("Only files may be selected, not folders.")

            elif commands[0] == 'select' and commands[1] in files:
                # COMMENT / REMOVE THIS BLOCK OF CODE IF SELECTION OF FILES IS NOT PERMITTED 
                
                print(colors["reset"], end='')
                return curr_dir + '/' + commands[1]

            # elif commands[0] == 'select' and commands[1] in files: # This prevents user from "selecting" a file instead of a folder.
            #     # COMMENT / REMOVE THIS BLOCK OF CODE OUT IF SELECTION OF FILES IS PERMITTED. 

            #     print("Only folers may be selected, not files.")
            

            elif commands[0] not in ['Exit', 'exit']:
                print(f'Not a valid option.')
        

        return None # Returns None as catch-all
    
    @staticmethod
    def switch_dir(old_dir: str, new_dir: str) -> str:
        dirs = new_dir.split('/')  # Splits user-inputted directory by folder, into list.
        temp_dir = old_dir.split('/')  # Splits old directory by folder, into list. This list will be used to create new path string
        
        dot_count = 0 # Used to count instances of ".." in input
        dir_add = [] # List of folders to be added to temp_dir

        input_contains_dots = ( ('..' in new_dir) or ('../' in new_dir) ) # Storing boolean in variable to prevent repeated checks.

        for i in range(len(dirs) - 1, -1, -1):  # Parses directory inputted to determine how to manipulate path string.
            # Iterating in reverse to prevent items from being skipped in list due to shifting.

            if input_contains_dots and dirs[i] == '..':
                dot_count += 1
            
            elif dirs[i] == '':  # Removing empty strings in dirs to prevent FileNotFound error
                dirs.remove(dirs[i])
            
            else:
                dir_add.append(dirs[i])  # Adds entry to dir_add, so it can be appended to temp_dir
        

        for i in range(0, dot_count): # Removes folders from old directory list
            temp_dir.remove(temp_dir[len(temp_dir) - 1])
    
        for folder in dir_add:
            temp_dir.append(folder)

        
        new_dir = ''

        for i in range(1, len(temp_dir)):  # Appends new folders to path string. Starts at index 1 to skip empty string at 0
            new_dir += f'/{temp_dir[i]}'
        
        if new_dir == '':  # This accounts for scenario for if user goes up to root directory with ".."
            new_dir = '/'

        if Menu.check_dir(new_dir, init_colors()):  # If directory is invalid, error message will be printed in check_dir()
            return new_dir
        
        return old_dir

    @staticmethod
    def check_dir(input_dir: str, colors: dict[str, str]) -> bool:  # Checks if directory exists and is accessible, and prints out specific error message if not.
        try:
            scandir(input_dir)
        
        except (FileNotFoundError, NotADirectoryError):
            print(f'{colors["clear"]}Not a valid directory.')
            return False
        
        except PermissionError:
            print(f'{colors["clear"]}Directory not accessible; permission denied.')
            return False
        
        return True

    @staticmethod
    def get_dir_contents(input_dir: str, colors: dict[str, str]) -> tuple[list[str], list[str]]: # Prints and returns all files and folders in directory
        
        files, folders, = [], []
        
        if Menu.check_dir(input_dir, colors):
            curr_dir = scandir(input_dir)  # Scans inputted directory.
        
            for entry in curr_dir:  # Sorts entries from iterator into folder and file lists for sorted output when printing directories.

                if entry.is_file():
                    files.append(entry.name)
        
                elif entry.is_dir():
                    folders.append(entry.name)
        

        Menu.print_dir(input_dir, files, folders, colors)
        return (files, folders)

    @staticmethod
    def print_dir(input_dir: str, files: list[str], folders: list[str], colors: dict[str, str]) -> None:

        print(f'{colors["reset"]}[*] {colors["path_col"]}{input_dir}{colors["reset"]}')  # Prints out path of current directory.
        
        if len(folders) == 0 and len(files) == 0:  # Prints special message for if directory is empty.
            print(fr'{colors["bold"]} \-> No content in this directory')
        
        else:  # Prints out content in directory, with folders listed before files.
            for i in range(0, len(folders)):

                if i % 2 == 0: # Alternating highlighting for folders and files
                    print(fr'{colors["folder_col1"]} \-> {folders[i]}{colors["reset"]}')
                
                else:
                    print(fr' {colors["folder_col2"]}\-> {folders[i]}{colors["reset"]}')
            
            for i in range(0, len(files)):

                if i % 2 == 0:
                    print(fr'{colors["file_col1"]} \-> {files[i]}{colors["reset"]}')

                else:
                    print(fr' {colors["file_col2"]}\-> {files[i]}{colors["reset"]}')
