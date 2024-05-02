import argparse
import json
from datetime import datetime
from typing import Optional

class File:

    def __init__(self, name: str, size: int, time_modified: int, permissions: str) -> None:
        '''
        Initialize a File object.

        Args:
            name (str): Name of the file.
            size (int): Size of the file in bytes.
            time_modified (int): Time when the file was last modified (UNIX timestamp).
            permissions (str): File permissions.
        '''

        self.name = name
        self.size = self.readable_size(size)
        self.time_modified = self.readable_timestamp(time_modified)
        self.permissions = permissions

    def readable_timestamp(self, time_modified: int) -> str:
        '''
        Convert UNIX timestamp to formatted date and time string.
        
        Args:
            time_modified (int): Time when the file was last modified (UNIX timestamp).
        
        Returns:
            str: Formatted date and time string.
        '''

        obj = datetime.fromtimestamp(time_modified)
        date_time = obj.strftime('%b %d %H:%M')
        return date_time
    
    def readable_size(self, size: int) -> str:
        '''
        Convert file size to a human-readable string.
                
        Args:
            size (int): Size of the file in bytes.
        
        Returns:
            str: Human-readable file size string.
        '''
        
        kb_size = size/ 1024.0
        mb_size = kb_size/ 1024.0
        if mb_size >= 1:
            return f"{mb_size:.1f}M"
        if kb_size >= 1:
            return f"{kb_size:.1f}K"
        return f"{size}"

    
class Directory:

    def __init__(self, name: str, size: int, time_modified: int, permissions: str, contents: list[File]) -> None:
        '''
        Initialize a Directory object.
        
        Args:
            name (str): Name of the directory.
            size (int): Size of the directory in bytes.
            time_modified (int): Time when the directory was last modified (UNIX timestamp).
            permissions (str): Directory permissions.
            contents (list[File]): List of contents (files).
        '''

        self.name = name
        self.size = self.readable_size(size)
        self.time_modified = self.readable_timestamp(time_modified)
        self.permissions = permissions
        self.contents = contents

    
    def readable_timestamp(self, time_modified: int) -> str:
        '''
        Convert UNIX timestamp to formatted date and time string.
        
        Args:
            time_modified (int): Time when the directory was last modified (UNIX timestamp).
        
        Returns:
            str: Formatted date and time string.
        '''

        obj = datetime.fromtimestamp(time_modified)
        date_time = obj.strftime('%b %d %H:%M')
        return date_time
    
    def readable_size(self, size: int) -> str:
        '''
        Convert file size to a human-readable string.
                
        Args:
            size (int): Size of the directory in bytes.
        
        Returns:
            str: Human-readable file size string.
        '''
        
        kb_size = size/ 1024.0
        mb_size = kb_size/ 1024.0
        if mb_size >= 1:
            return f"{mb_size:.1f}M"
        if kb_size >= 1:
            return f"{kb_size:.1f}K"
        return f"{size}"

  
def print_details(data: list[object]) -> None:
    '''
    Print detailed information for each file and directory.
    
    Args:
        data (List[object]): List of objects containing file and directory information.
    '''

    for item in data:
        print(f"{item.permissions: >10} {item.size: >4} {item.time_modified: >12} {item.name}")


def path_contents(contents: list[object], directory_path: str) -> Optional[list[object]]:
    '''
    Get the contents of a directory specified by the path.
    
    Args:
        contents (List[object]): List of objects containing file and directory information.
        directory_path (str): Path of the directory.
    
    Returns:
        Optional[List[object]]: Contents of the specified directory. None if directory doesn't exist.
    '''

    path_list = directory_path.split('/')
    names = [item.name for item in contents]
    if path_list[0] not in names:
        return None
    
    for name in path_list:
        for item in contents:
            if item.name == name and isinstance(item, File):
                contents = [item,]
            if item.name == name and isinstance(item, Directory):
                contents = item.contents

    if len(path_list) > 1 and len(contents) == 1:
        contents[0].name = './' + str(directory_path)
    
    return contents


def main() -> None:
    '''
    Main function to parse command line arguments and display directory contents.
    '''

    parser = argparse.ArgumentParser(description='List files and directories.', add_help=False)
    parser.add_argument('directory', nargs='?', default='.', help='Specify the directory to list. If not provided, the current directory will be listed')
    parser.add_argument('-A', action='store_true', help='Show all files and directories, including hidden ones')
    parser.add_argument('-l', action='store_true', help='Show detailed information for each file and directory')
    parser.add_argument('-r', action='store_true', help='Reverse the order of listing')
    parser.add_argument('-t', action='store_true', help='Sort files and directories by modification time')
    parser.add_argument('--filter', default='default', choices = ['dir', 'file'], help='Filter the output based on the given option (dir or file)')
    parser.add_argument('-h', '--help', action='help', help='Show all help messages and exit')
        
    args = parser.parse_args()
    directory_path = args.directory
    contents = []

    try:
        with open('directory.json') as f:

            data = json.load(f)
            for item in data['contents']:

                if item.get('contents'):
                    directory_contents = []
                    for file_data in item['contents']:
                        directory_contents.append(File(file_data['name'], file_data['size'], file_data['time_modified'], file_data['permissions']))
                    directory = Directory(item['name'], item['size'], item['time_modified'], item['permissions'], directory_contents)
                    contents.append(directory)

                else:
                    contents.append(File(item['name'], item['size'], item['time_modified'], item['permissions']))
                    

    except Exception as e:
        print(e)

    if not args.A:
        contents = [item for item in contents if not item.name.startswith('.')]
    
    if args.directory != '.' and args.directory != './':
        contents = path_contents(contents=contents, directory_path=directory_path)
        if not contents:
            print(f"error: cannot access '{directory_path}': No such file or directory")
            return

    if args.t:
        contents.sort(key = lambda x: x.time_modified)

    if args.filter != 'default':
        if args.filter == 'file':
            contents = [item for item in contents if isinstance(item, File)]

        elif args.filter == 'dir':
            contents = [item for item in contents if isinstance(item, Directory)]

        # else:
        #     print(f"error: '{args.filter}' is not a valid filter criteria. Available filters are 'dir' and 'file'")
        #     return
    
    if args.r:
        contents = reversed(contents)

    if args.l:
        print_details(contents)

    else:
        contents = [item for item in contents]
        print(" ".join([item.name for item in contents]))
        
if __name__ == '__main__':
    main()
