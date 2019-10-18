from listdir import listdir
import os
import time

testfile = "testfile"
filepath = "testfile.txt"
filepath2 = "testfile2.txt"
filepath3 = "testfile2.txt"
timestr = time.strftime("%Y%m%d-%I%M%S %p")

def test_zip_save():
    assert listdir.zip_save(filepath,f'{testfile} {listdir.timestamp_name()}') == listdir.zip_save(filepath,f'{testfile} {timestr}')

def test_timestamp_name():
    assert (f'{testfile} {listdir.timestamp_name()}') == (f'{testfile} {timestr}')

def test_csv_save():
    assert listdir.csv_save(filepath,f'{testfile} {listdir.timestamp_name()}')  == listdir.csv_save(filepath,f'{testfile} {timestr}')

def test_sha1_hash():
    assert listdir.sha1_hash(filepath), "6a4b4559254b5f6f9b1f23bac25b075f7fc5a05c"
    assert listdir.sha1_hash(filepath2), "da39a3ee5e6b4b0d3255bfef95601890afd80709"

def test_md5_hash():
    assert listdir.md5_hash(filepath), "032ca7234a799c1b56d198d6ff321fc0"


if __name__ == '__main__':
    unittest.main()
