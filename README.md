# listdir.py
listdr.py is a script that will ask the user to provide a directory and the script will search all files and subdirectories and save it to a CSV file.
The .csv file provides the parent directory, filename and the file size.

## Usage
To use the script, do the following. The user **MUST** provide an existing directory and a csv filename.
```python
python listdir.py <directory> <csv filename>
```
For more info, the code below shows the -h for the script.
```python
usage: listdir.py [-h] path csvfilename

positional arguments:
  path         Path directory
  csvfilename  CSV filename to be saved

optional arguments:
  -h, --help   show this help message and exit
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

# project-structure
