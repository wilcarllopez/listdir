import os, glob, csv, argparse, hashlib
import zipfile as zip
import configparser
#Variable for csv file
csv_file = []
directory = []
#end of variable declaration

#Start of functions
def find_path(path,csvfilename):
    """Finding the directory of the pathname path"""
    os.chdir(path)
    if os.path.exists(path) == True:
        csv_save(path,csvfilename)
    else:
        return "Path directory doesn't exists"

def zip_save(csvfilename):
    with zip.ZipFile(f"{csvfilename}.zip", 'w') as zipFile:
        zipFile.write(csvfilename)

def csv_save(path, csvfilename):
    """After completing the find_path function, csv_save function will get the files and subdirectories of the path provided
     by the user. Then it will be save as a csv file, name provided by the user."""
    blocksize = 65536
    hasher = hashlib.md5()
    hasher2 = hashlib.sha1()
    with open(f"{csvfilename}.csv",'w+', newline='') as csvFile:
        headwriter = csv.DictWriter(csvFile, fieldnames = ["Parent Directory","Filename","File Size", "MD5", "SHA-1"])
        headwriter.writeheader()
        writer = csv.writer(csvFile, delimiter=",")
        for r,d,files in os.walk(path):
            for f in files:
                filepath ="{}\{}".format(r,f)
                with open(filepath,'rb') as file:
                    buf = file.read(blocksize)
                    while len(buf) > 0:
                        hasher.update(buf)
                        hasher2.update(buf)
                        buf = file.read(blocksize)
                md5 = hasher.hexdigest()
                sha1 = hasher2.hexdigest()
                size = os.path.getsize(filepath)
                row = [str(r), f, size, md5, sha1]
                writer.writerow(row)
    zip_save(f"{csvfilename}.csv")

#end of functions

if __name__== "__main__":
    config = configparser.ConfigParser()
    config.read('listdir_hash.ini')
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs="?", default=config['default']['path'],help = 'Path directory')
    parser.add_argument('csvfilename', nargs="?",default=config['default']['csvfilename'],help = 'CSV filename to be saved')
    args = parser.parse_args()

    path = args.path
    csvfilename = args.csvfilename
    find_path(path,csvfilename)
