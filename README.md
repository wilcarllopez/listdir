# listdir.py (JSON save, CSV save, Database save)
listdr.py is a script that will ask the user to provide a directory and the script will search all files and subdirectories and save it to a CSV file.
The .csv file provides the parent directory, filename and the file size, md5, sha1.
## Update
Added a config file called config.ini file where it will run a default value from the config file if the user didn't input anything.
Added JSON save, where user can save the found directory to a JSON file.
Added Database save, where user can save the found directory to a database. 
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
## Pytest
To use the test.py from the .\tests folder. User must install pytest.
To use test, type the following:
```
pytest test.py
```
To check the coverage, install pytest-cov then type:
```
pytest --cov=listdir test.py
```
Below shows the coverage
```
Name                                                                      Stmts   Miss  Cover
---------------------------------------------------------------------------------------------
C:\Users\TEU_USER\Documents\Python Training\listdir\listdir\__init__.py       1      0   100%
C:\Users\TEU_USER\Documents\Python Training\listdir\listdir\listdir.py       70     24    66%
---------------------------------------------------------------------------------------------
TOTAL                                                                        71     24    66%
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

# project-structure
