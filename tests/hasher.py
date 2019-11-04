import hashlib
blocksize = 65536
hasher = hashlib.sha1()
with open("testfile2.txt", 'rb') as file:
    buf = file.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = file.read(blocksize)
sha1 = hasher.hexdigest()
print(sha1)