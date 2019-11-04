import argparse
import configparser
import csv
import hashlib
import time
import zipfile as zip
import logging.config
import os
import logging
import yaml
import sys
import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import getpass

# Start of class
class Password(argparse.Action):
    """Class to set password to be hidden"""
    def __call__(self, parser, namespace, values, option_string=None):
        if values is None:
            values = getpass.getpass()
        setattr(namespace, self.dest, values)
# End of class
# Start of functions
def setup_logging(default_path='loggingConfig.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setting up the logging config"""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print('Error in Logging Configuration. Using default configs', e)
                logging.basicConfig(level=default_level, stream=sys.stdout)
    else:
        logging.basicConfig(level=default_level, stream=sys.stdout)
        print('Failed to load configuration file. Using default configs')

def config(section='postgresql'):
    """"""
    config = configparser.ConfigParser()
    dir = os.path.dirname(os.path.abspath(__file__))
    config.read(dir + os.sep + 'config.ini')
    db = {}
    if config.has_section(section):
        params = config.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the file'.format(section))
    return db

def dbase_connect(password, path):
    """Connects to a database and CRUD function"""
    global connection
    try:
        params = config()
        connection = psycopg2.connect(password = password,**params)
        cursor = connection.cursor()
        cursor.execute("SELECT exists(SELECT 1 from pg_catalog.pg_database WHERE datname = 'listdir_db');")

        if cursor.fetchone()[0]:
            connection = psycopg2.connect(password=password, database='listdir_db', **params)
            cursor = connection.cursor()
            logger.info("Connected to the database")
            cursor.execute("SELECT to_regclass('test');")
            if cursor.fetchone()[0]:
                for r, d, files in os.walk(path):
                    for f in files:
                        filepath = "{}{}{}".format(r, os.sep, f)
                        size = os.path.getsize(filepath)
                        md5 = md5_hash(filepath)
                        sha1 = sha1_hash(filepath)
                        row = (str(r), f, size, md5, sha1)
                        insert_table_query = '''INSERT INTO test (DIRECTORY, FILENAME, FILESIZE, MD5, SHA1) 
                                                                                                values (%s, %s, %s, %s, %s)'''
                        cursor.execute(insert_table_query, row)
                        connection.commit()
            else:
                create_table_query = '''CREATE TABLE test(
                                                    ID SERIAL PRIMARY KEY,
                                                    DIRECTORY VARCHAR NOT NULL,
                                                    FILENAME VARCHAR NOT NULL,
                                                    FILESIZE INT NOT NULL,
                                                    MD5 VARCHAR NOT NULL,
                                                    SHA1 VARCHAR NOT NULL,
                                                    created_at TIMESTAMP DEFAULT NOW()
                                                    )'''
                cursor.execute(create_table_query)
                logger.info("Successfully created a database table 'test'")
                connection.commit()
                for r, d, files in os.walk(path):
                    for f in files:
                        filepath = "{}{}{}".format(r, os.sep, f)
                        size = os.path.getsize(filepath)
                        md5 = md5_hash(filepath)
                        sha1 = sha1_hash(filepath)
                        row = (str(r), f, size, md5, sha1)
                        insert_table_query = '''INSERT INTO test (DIRECTORY, FILENAME, FILESIZE, MD5, SHA1) 
                                                                                                values (%s, %s, %s, %s, %s)'''
                        cursor.execute(insert_table_query, row)
                        connection.commit()

            connection.commit()
            cursor.close()
            connection.close()
            logger.info("Successfully inserted values to database table 'test'")
        else:
            create_database = '''CREATE DATABASE listdir_db;'''
            cursor.execute(create_database)
            connection.commit()
            logger.info("Successfully created database 'listdir_db'")
            connection = psycopg2.connect(password = password, database = 'listdir_db', **params)
            cursor = connection.cursor()
            create_table_query = '''CREATE TABLE test(
                                                    ID SERIAL PRIMARY KEY,
                                                    DIRECTORY VARCHAR NOT NULL,
                                                    FILENAME VARCHAR NOT NULL,
                                                    FILESIZE INT NOT NULL,
                                                    MD5 VARCHAR NOT NULL,
                                                    SHA1 VARCHAR NOT NULL,
                                                    created_at TIMESTAMP DEFAULT NOW()
                                                    )'''
            cursor.execute(create_table_query)
            connection.commit()
            logger.info("Successfully created a database table 'test'")
            for r, d, files in os.walk(path):
                for f in files:
                    filepath = "{}{}{}".format(r, os.sep, f)
                    size = os.path.getsize(filepath)
                    md5 = md5_hash(filepath)
                    sha1 = sha1_hash(filepath)
                    row = (str(r), f, size, md5, sha1)
                    insert_table_query = '''INSERT INTO test (DIRECTORY, FILENAME, FILESIZE, MD5, SHA1) 
                                                                                values (%s, %s, %s, %s, %s)'''
                    cursor.execute(insert_table_query, row)
                    connection.commit()

            cursor.close()
            connection.close()
            logger.info("Successfully inserted values to database table 'test'")
        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        logger.error("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            logger.info("PostgreSQL connection is closed")

def find_path(path):
    """Finding the directory of the pathname path"""
    try:
        logger.info("Finding the path: " + path)
        os.chdir(path)
        if os.path.exists(path) is True:
            logger.info("Path: " + path +" found!")
            return True
        else:
            logger.error("Path directory doesn't exists")
            sys.exit()
    except FileNotFoundError:
        logger.error("Path directory doesn't exists")
        sys.exit()

def sha1_hash(filepath):
    """Hashing the file through SHA-1"""
    try:
        blocksize = 65536
        hasher = hashlib.sha1()
        with open(filepath, 'rb') as file:
            buf = file.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = file.read(blocksize)
        sha1 = hasher.hexdigest()
        logger.info("Hashed the file: "+ filepath + " - SHA-1 Value:" + sha1)
        return sha1
    except:
        logger.error("Unable to hash file through SHA-1")

def md5_hash(filepath):
    """Hashing the file through MD5"""
    try:
        blocksize = 65536
        hasher = hashlib.md5()
        with open(filepath, 'rb') as file:
            buf = file.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = file.read(blocksize)
        md5 = hasher.hexdigest()
        logger.info("Hashed the file: " + filepath + " - MD5 Value:" + md5)
        return md5
    except:
        logger.error("Unable to hash file through MD5")

def csv_save(path, csvfilename):
    """csv_save function will get the files and subdirectories of the path provided
     by the user. Then it will be save as a csv file, name provided by the user."""
    global finalfilename
    try:
        finalfilename = f"{csvfilename} {str(timestamp_name())}.csv"
        with open(finalfilename, 'w+', newline='') as csvFile:
            logger.info("Created a csv file named: " + finalfilename)
            headwriter = csv.DictWriter(csvFile, fieldnames=["Parent Directory", "Filename", "File Size", "MD5", "SHA-1"])
            headwriter.writeheader()
            writer = csv.writer(csvFile, delimiter=",")
            for r, d, files in os.walk(path):
                for f in files:
                    filepath = "{}{}{}".format(r, os.sep, f)
                    size = os.path.getsize(filepath)
                    md5 = md5_hash(filepath)
                    sha1 = sha1_hash(filepath)
                    row = [str(r), f, size, md5, sha1]
                    writer.writerow(row)
                    logger.info("The filename: " + f + " with directory: " + str(r) + " size: " + str(size) + " with corresponding MD5 and SHA-1 values was added to CSV file")
    except:
        logger.error("Unable to write CSV file")
    logger.info("Created a time string info of year,month,date-hour,min,second and meridian: " + timestamp_name())
    logger.info("Successfully created " + finalfilename)
    zip_save(finalfilename, csvfilename)
    return 'Success'

def json_save(path, csvfilename):
    """csv_save function will get the files and subdirectories of the path provided
     by the user. Then it will be save as a csv file, name provided by the user."""
    global finalfilename
    try:
        finalfilename = f"{csvfilename} {str(timestamp_name())}.json"
        with open(finalfilename, 'w+', newline='') as jsonFile:
            logger.info("Created a json file named: " + finalfilename)
            for r, d, files in os.walk(path):
                for f in files:
                    filepath = "{}{}{}".format(r, os.sep, f)
                    size = os.path.getsize(filepath)
                    md5 = md5_hash(filepath)
                    sha1 = sha1_hash(filepath)
                    data = {}
                    data[f]=[]
                    data[f].append({
                        'Parent Directory' : str(r),
                        "Filename": f,
                        "File Size": size,
                        "MD5": md5,
                        "SHA-1": sha1
                    })
                    json.dump(data, jsonFile, indent=2)
                    logger.info("The filename: " + f + " with directory: " + str(r) + " size: " + str(size) + " with corresponding MD5 and SHA-1 values was added to JSON file")
    except:
        logger.error("Unable to write a JSON file")
    logger.info("Created a time string info of year,month,date-hour,min,second and meridian: " + timestamp_name())
    logger.info("Successfully created " + finalfilename)
    zip_save(finalfilename, csvfilename)
    return 'Success'

def timestamp_name():
    """Updates the time and date for .ini file"""
    try:
        timestr = time.strftime("%Y%m%d-%I%M%S %p")
        return timestr
    except:
        logger.error("Unable to create time stamp name")
def zip_save(finalfilename, csvfilename):
    """Save the csv file to zip file"""
    try:
        compression = zip.ZIP_DEFLATED
    except:
        compression = zip.ZIP_STORED
    try:
        with zip.ZipFile(f'{csvfilename} {str(timestamp_name())}.zip', 'w', compresslevel=None) as zipFile:
            zipFile.write(finalfilename, compress_type=compression)
            logger.info("Successfully created a zip file named: " + f'{csvfilename} {str(timestamp_name())}.zip')
    except:
        logger.error("Unable to create zip file")

def main():


    """Main function of the program"""
    # Updates the config file
    config = configparser.ConfigParser()
    dir = os.path.dirname(os.path.abspath(__file__))
    config.read(dir + os.sep + 'config.ini')
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs="?", default=config['default']['path'], help='Path directory')
    parser.add_argument('csvfilename', nargs="?", default=config['default']['csvfilename'],
                        help='CSV filename to be saved')
    parser.add_argument('-j','--js', action='store_true', help='Writes the file to json')
    parser.add_argument('-c', '--csv', action='store_true', help='Writes the file to csv')
    parser.add_argument('-p', '--postgres', action='store_true', help='Writes the file to a database')
    parser.add_argument("-pwd", "--password", action=Password, nargs='?', dest='password',
                        help='Password for the database')
    args = parser.parse_args()
    # Setting up variables
    path = os.path.abspath(args.path)
    csvfilename = args.csvfilename
    # Start of the program
    if args.js:
        find_path(path)
        json_save(path,csvfilename)
    elif args.csv:
        find_path(path)
        csv_save(path, csvfilename)
    elif args.postgres:
        password = args.password
        dbase_connect(password, path)
# end of functions

if __name__ == "__main__":
    setup_logging() #Setting up the logging config
    logger = logging.getLogger(__name__)
    logger.info("Creating new log file")
    logger.info("Logging setup completed")
    main()
