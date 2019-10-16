import argparse
import configparser
import csv
import hashlib
import os
import time
import zipfile as zip

# Start of functions
def find_path(path, csvfilename):
    """Finding the directory of the pathname path"""
    os.chdir(path)
    if os.path.exists(path) == True:
        csv_save(path, csvfilename)
    else:
        return "Path directory doesn't exists"

def sha1_hash(filepath):
    """Hashing the file through SHA-1"""
    blocksize = 65536
    hasher = hashlib.sha1()
    with open(filepath, 'rb') as file:
        buf = file.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = file.read(blocksize)
    sha1 = hasher.hexdigest()
    return sha1

def md5_hash(filepath):
    """Hashing the file through MD5"""
    blocksize = 65536
    hasher = hashlib.md5()
    with open(filepath, 'rb') as file:
        buf = file.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = file.read(blocksize)
    md5 = hasher.hexdigest()
    return md5


def csv_save(path, csvfilename):
    """csv_save function will get the files and subdirectories of the path provided
     by the user. Then it will be save as a csv file, name provided by the user."""
    config = configparser.ConfigParser()
    config.read('listdir_hash.ini')
    datetime=config['datetime']['timestr']
    with open(f"{csvfilename} {datetime}.csv", 'w+', newline='') as csvFile:
        headwriter = csv.DictWriter(csvFile, fieldnames=["Parent Directory", "Filename", "File Size", "MD5", "SHA-1"])
        headwriter.writeheader()
        writer = csv.writer(csvFile, delimiter=",")
        for r, d, files in os.walk(path):
            for f in files:
                filepath = "{}\{}".format(r, f)
                size = os.path.getsize(filepath)
                md5 = md5_hash(filepath)
                sha1 = sha1_hash(filepath)
                row = [str(r), f, size, md5 , sha1 ]
                writer.writerow(row)
    zip_save(f"{csvfilename}.csv")


def update_ini():
    """Updates the time and date for .ini file"""
    config = configparser.RawConfigParser()
    config.read('listdir_hash.ini')
    timestr = time.strftime("%Y%m%d-%I%M%S%p")
    try:
        config.set('datetime', 'timestr', timestr)
        with open("listdir_hash.ini", 'w+') as cfgfile:
            config.write(cfgfile)
    except config.NoSectionError:
        # Create non-existent section
        config.add_section('datetime')
        config.set('datetime', 'timestr', timestr)
        with open("listdir_hash.ini", 'w+') as cfgfile:
            config.write(cfgfile)

def zip_save(csvfilename):
    """Save the csv file to zip file"""
    config = configparser.ConfigParser()
    config.read('listdir_hash.ini')
    datetime = config['datetime']['timestr']
    with zip.ZipFile(f"{csvfilename} {datetime}.zip", 'w') as zipFile:
        zipFile.write(csvfilename)
# end of functions


if __name__ == "__main__":
    #Updates the config file
    update_ini()
    config = configparser.ConfigParser()
    config.read('listdir_hash.ini')
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs="?", default=config['default']['path'], help='Path directory')
    parser.add_argument('csvfilename', nargs="?", default=config['default']['csvfilename'],
                        help='CSV filename to be saved')
    args = parser.parse_args()
    #Setting up variables
    path = args.path
    csvfilename = args.csvfilename
    #Start of the program
    find_path(path, csvfilename)
