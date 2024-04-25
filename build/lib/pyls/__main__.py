import argparse
import json
from datetime import datetime


def cal_date_time(value):
    obj = datetime.utcfromtimestamp(value)
    date_time = obj.strftime('%b %d %H:%M')
    return date_time

def cal_size(size):
    if size>1023:
        size_kb = size/1024.0
        if size_kb>1023:
            size_mb = round((size_kb/1024.0), 1)
            return str(size_mb)+'M'
        else:
            size_kb = round(size_kb, 1)
            return str(size_kb)+'K'
    else:
        return size
    

def print_details(data):
    
    for item in data:
        date_time = cal_date_time(item['time_modified'])
        size = cal_size(item['size'])
        print(f"{item['permissions']: <11}{size: <6}{date_time: <13}{item['name']}")


def path_contents(contents, path_list):
    path = '.'
    for i in range (len(path_list)):
        path = path+'/'+str(path_list[i])
        names = [item['name'] for item in contents]
        new_contents = []
        if path_list[i] in names:
            for item in contents:
                if item['name'] == path_list[i] and item.get('contents'):
                    new_contents = [j for j in item['contents']]
                    contents = [j for j in item['contents']]
                elif  item['name'] == path_list[i]:
                    new_contents = []
                    new_contents.append(item)
    
    if len(new_contents) <0:
        return
    if len(path_list) > 1 and len(contents) == 1:
        new_contents[0]['name'] = path

    return new_contents


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', nargs='?',default='.', help="Show directory details")
    parser.add_argument('-A', action='store_true', help='Show all directory')
    parser.add_argument('-l', action='store_true', help='Show all directory details')
    parser.add_argument('-r', action='store_true', help='Show all directory details in reverse')
    parser.add_argument('-t', action='store_true', help='Show all directory details sorted by modification time')
    parser.add_argument('--filter', default='default', choices=['dir', 'file'], help='Show details according to the filter')

    args = parser.parse_args()
    directory_path = args.directory
    path_list = directory_path.split('/')

    with open('directory.json') as f:
    
        data = json.load(f)
        contents = data['contents']
            
        if not args.A:
            contents = [item for item in contents if not item['name'].startswith('.')]

        if args.directory == '.':
            pass
        elif path_list:
            contents = path_contents(contents=contents, path_list=path_list)
            if not contents:
                print(f"error: cannot access '{directory_path}': No such file or directory")
                return

        if args.t:
            contents.sort(key = lambda x: x.get('time_modified', 0))

        if args.filter == 'default':
            pass

        elif args.filter == 'file':
            contents = [item for item in contents if not item.get('contents')]

        elif args.filter == 'dir':
            contents = [item for item in contents if item.get('contents')]

        else:
            print(f"error: '{args.filter}' is not a valid filter criteria. Available filters are 'dir' and 'file'")
            return
        
        if args.r:
            contents = reversed(contents)

        if args.l:
            print_details(contents)

        else:
            contents = [item for item in contents]
            print(" ".join([item['name'] for item in contents]))
        

if __name__ == '__main__':
    main()
