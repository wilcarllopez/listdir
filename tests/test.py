from listdir import listdir
import os
import time

testfile = "testfile"
timestr = time.strftime("%Y%m%d-%I%M%S %p")
#def test_find_path(self):
#    self.assertEqual(listdir.find_path(".",""))

def test_timestamp_name():
    assert (f'{testfile} {listdir.timestamp_name()}') == (f'{testfile} {timestr}')

#def test_sha1_hash():
#    self.assertEqual(listdir.sha1_hash("./test/testfile.txt"), "098f6bcd4621d373cade4e832627b4f6")

if __name__ == '__main__':
    unittest.main()