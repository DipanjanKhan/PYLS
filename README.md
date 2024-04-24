
# pyls

'pyls' is a Python program that lists the contents of a directory in the style of the ls (Linux utility).



## Installation

Install 'pyls' using command prompt:

Navigate to the project directory:
```bash
  cd pyls
```

Run the installation command:
```bash
  pip install .
```

    
## Usage/Examples

Run the pyls command followed by any optional arguments:

```bash
pyls [directory] [-A] [-l] [-r] [-t] [--filter=<option>]
```

'[directory]' (optional) : Specify the directory to list. If not provided, the current directory will be listed.

'-A' : Show all files and directories, including hidden ones.

'-l' : Show detailed information for each file and directory.

'-r' : Reverse the order of listing.

'-t' : Sort files and directories by modification time.

'--filter=<option>' : Filter the output based on the given option (dir or file).

For example:
```bash
    pyls -l -r -t --filter=file
```
Output:
```bash
-rw-r--r-- 74    Nov 14 13:57 main.go
drwxr-xr-x 60    Nov 14 13:51 go.mod
drwxr-xr-x 83    Nov 14 11:27 README.md
drwxr-xr-x 1.0K  Nov 14 11:27 LICENSE
```