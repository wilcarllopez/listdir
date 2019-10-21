from listdir import *
import time
import pytest
import os
import hashlib
import logging

path = os.path.dirname(os.path.abspath(__file__))
testfile = ["testfile", "testfile2" , "testfile3", "testfile4", "testfile5"]
filelist = ["testfile.txt","testfile2.txt","testfile3.txt"]
filepath = "testfile.txt"
filepath2 = "testfile2.txt"
filepath3 = "testfile3.txt"
timestr = time.strftime("%Y%m%d-%I%M%S %p")

def test_zip_save():
    for text in filelist:
        blocksize = 65536
        hasher = hashlib.sha1()
        with open(text, 'rb') as file:
            buf = file.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = file.read(blocksize)
        sha1 = hasher.hexdigest()
        assert listdir.zip_save(filepath,f'{sha1} {listdir.timestamp_name()}') == listdir.zip_save(filepath,f'{sha1} {timestr}')

def test_timestamp_name():
    for file in testfile:
        assert (f'{file} {listdir.timestamp_name()}') == (f'{file} {timestr}')

def test_csv_save():
    for file in testfile:
        assert listdir.csv_save(filepath,f'{file} {listdir.timestamp_name()}')  == listdir.csv_save(filepath,f'{file} {timestr}')

def test_json_save():
    for file in testfile:
        assert listdir.json_save(filepath,f'{file} {listdir.timestamp_name()}')  == listdir.json_save(filepath,f'{file} {timestr}')

def test_sha1_hash():
    assert listdir.sha1_hash(filepath), "6a4b4559254b5f6f9b1f23bac25b075f7fc5a05c"
    assert listdir.sha1_hash(filepath2), "da39a3ee5e6b4b0d3255bfef95601890afd80709"

def test_md5_hash():
    assert listdir.md5_hash(filepath), "032ca7234a799c1b56d198d6ff321fc0"

def test_find_path():
    assert os.path.exists(path)
    assert listdir.find_path(path) == True

if __name__ == '__main__':
    pytest.main()
