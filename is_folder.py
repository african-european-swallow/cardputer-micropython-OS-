import os

def is_dir(name):
    try:
        return (os.stat(name)[0] & 0x4000) != 0
    except:
        return False

for name in os.listdir():
    if is_dir(name):
        print(name, "is a folder")
    else:
        print(name, "is a file")
