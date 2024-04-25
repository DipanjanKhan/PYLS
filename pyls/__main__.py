import argparse
import json
from datetime import datetime
from typing import Optional



def cal_date_time(value: int) -> str:
    '''
    Convert UNIX timestamp to formatted date and time string.
    
    Args:
        value (int): UNIX timestamp.
    
    Returns:
        str: Formatted date and time string.
    '''

    obj = datetime.fromtimestamp(value)
    date_time = obj.strftime('%b %d %H:%M')
    return date_time

def cal_size(size: int) -> str:
    '''
    Convert file size to a human-readable string.
    
    Args:
        size (int): File size in bytes.
    
    Returns:
        str: Human-readable file size string.
    '''
    
    kb_size = size/ 1024.0
    mb_size = kb_size/ 1024.0
    if mb_size >= 1:
        return f"{mb_size:.1f}M"
    elif kb_size >= 1:
        return f"{kb_size:.1f}K"
    else:
        return f"{size}"
    

def print_details(data: list[dict]) -> None:
    '''
    Print detailed information for each file and directory.
    
    Args:
        data (List[dict]): List of dictionaries containing file/directory information.
    '''

    for item in data:
        date_time = cal_date_time(item['time_modified'])
        size = cal_size(item['size'])
        print(f"{item['permissions']: >10} {size: >4} {date_time: >12} {item['name']}")


def path_contents(contents: list[dict], directory_path: str) -> Optional[list[dict]]:
    '''
    Get the contents of a directory specified by the path.
    
    Args:
        contents (List[dict]): List of dictionaries containing directory contents.
        directory_path (str): Path of the directory.
    
    Returns:
        Optional[List[dict]]: Contents of the specified directory. None if directory doesn't exist.
    '''
    path_list = directory_path.split('/')
    contents_dict = {item['name']: item for item in contents}
    
    for name in path_list:
        if name not in contents_dict:
            return None

        current_dir = contents_dict[name]
        if current_dir.get('contents'):
            contents = current_dir['contents']
            contents_dict = {item['name']: item for item in contents}
        else:
            contents = [current_dir]
    if len(path_list) > 1 and len(contents) == 1:
        contents[0]['name'] = './' + str(directory_path)
    
    return contents


def main() -> None:
    '''
    Main function to parse command line arguments and display directory contents.
    '''

    parser = argparse.ArgumentParser(description='List files and directories.', add_help=False)
    parser.add_argument('directory', nargs='?',default='.', help='Specify the directory to list. If not provided, the current directory will be listed')
    parser.add_argument('-A', action='store_true', help='Show all files and directories, including hidden ones')
    parser.add_argument('-l', action='store_true', help='Show detailed information for each file and directory')
    parser.add_argument('-r', action='store_true', help='Reverse the order of listing')
    parser.add_argument('-t', action='store_true', help='Sort files and directories by modification time')
    parser.add_argument('--filter', default='default',metavar="N", choices = ['dir', 'file'], help='Filter the output based on the given option (dir or file)')
    parser.add_argument('-h', '--help', action='help', help='Show all help messages and exit')

    # try:
    #     args = parser.parse_args()
    # except argparse.ArgumentError as exc:
    #     print(f"error: '{exc.argument_value}' is not a valid filter criteria. Available filters are 'dir' and 'file'")
    #     return
        
    args = parser.parse_args()
    directory_path = args.directory
    contents = []
    try:
        with open('directory.json') as f:
            data = json.load(f)
            contents = data['contents']
    except Exception as e:
        print(e)

     
    if not args.A:
        contents = [item for item in contents if not item['name'].startswith('.')]

    if args.directory != '.' and args.directory != './':
        contents = path_contents(contents=contents, directory_path=directory_path)
        if not contents:
            print(f"error: cannot access '{directory_path}': No such file or directory")
            return

    if args.t:
        contents.sort(key = lambda x: x.get('time_modified', 0))

    if args.filter != 'default':
        if args.filter == 'file':
            contents = [item for item in contents if not item.get('contents')]

        elif args.filter == 'dir':
            contents = [item for item in contents if item.get('contents')]

        # else:
        #     print(f"error: '{args.filter}' is not a valid filter criteria. Available filters are 'dir' and 'file'")
        #     return
    
    if args.r:
        contents = reversed(contents)

    if args.l:
        print_details(contents)

    else:
        contents = [item for item in contents]
        print(" ".join([item['name'] for item in contents]))
        
if __name__ == '__main__':
    main()
