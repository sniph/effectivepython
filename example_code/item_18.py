#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Copyright 2014-2019 Brett Slatkin, Pearson Education Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Reproduce book environment
import random

random.seed(1234)

import logging
from pprint import pprint
from sys import stdout as STDOUT

# Write all output to a temporary directory
import atexit
import gc
import io
import os
import tempfile

TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

# Make sure Windows processes exit cleanly
OLD_CWD = os.getcwd()#testfile location see python console for path then powershell cd 'path'
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)


def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()


atexit.register(close_open_files)


# Example 1
pictures = {}
path = "profile_1234.png"

with open(path, "wb") as f:
    f.write(b"image data here 1234")#write text to new file in byte code b"image data here 1234" like picture format
    #see getcwd() for location new file
# assign if key if not get genertes default "None"
if (handle := pictures.get(path)) is None:#assign item path of set pictures to var handle if exists
    # if "None" then try loop
    try:
        handle = open(path, "a+b")
    except OSError:
        print(f"Failed to open path {path}")
        raise
    else:
        pictures[path] = handle#assign new path to dict/set
print(handle)
print(pictures)#returns key/value from dict ->{'profile_1234.png': <_io.BufferedRandom name='profile_1234.png'>}
print(pictures['profile_1234.png'])#returns value part of key/value -><_io.BufferedRandom name='profile_1234.png'>
# set pointer to begin of set/file
handle.seek(0)
print(handle.seek(0))
# read the data from the handle into var image_data
image_data = handle.read()#read file data to var

print(pictures)
print(image_data)


# Example 2
# Examples using in and KeyError
pictures = {}
path = "profile_9991.png"

with open(path, "wb") as f:
    f.write(b"image data here 9991")#create new file with text b"image data here 9991"
# test path in picture then assign path from picture set to handle
if path in pictures:#if path exists
    handle = pictures[path]
# if not in pictures set then assign open path to handle
else:
    try:
        handle = open(path, "a+b")
    except OSError:
        print(f"Failed to open path {path}")
        raise
    # assign new handle to pictures set
    else:
        pictures[path] = handle #add key/value to dict
# set pointer to begin of handle(file/set/data)
handle.seek(0)
image_data = handle.read()#read content of file bytes to var

print(pictures)
print(image_data)#return text from new key

pictures = {}
path = "profile_9922.png"

with open(path, "wb") as f:#create new file and and byte text as picture
    f.write(b"image data here 9922")
# try on keyerror if key(path) is missing
# if exists assign key(path) to handle

print(pictures[path])#return keyerror
handle = pictures[path]#still prev handle
print(handle)
try:
    handle = pictures[path]#path not yet in dict
# if key missing assign new  key(path) to handle
except KeyError:#if not exists
    try:
        handle = open(path, "a+b")#cannot open
    except OSError:
        print(f"Failed to open path {path}")
        raise
    # and assign handle to set in pictures
    else:
        pictures[path] = handle#add from "handle = open(path, "a+b")" as content handle
print(handle)
# point to begin of handle
handle.seek(0)
# read value where handle is referencing to
image_data = handle.read()

print(pictures)
print(image_data)


# Example 3
pictures = {}
path = "profile_9239.png"

handle = pictures.setdefault(path, open(path, "a+b"))

with open(path, "wb") as f:
    f.write(b"image data here 9239")
# assign pictures(path) to handle if not in set pictures assign default path
try:
    handle = pictures.setdefault(path, open(path, "a+b"))
except OSError:
    print(f"Failed to open path {path}")
    raise
# point to begin of handle
# assign handle refering data to image_data
else:
    handle.seek(0)
    image_data = handle.read()#assign data to var

print(pictures)
print(image_data)


# Example 4
path = "profile_4555.csv"

with open(path, "wb") as f:
    f.write(b"image data here 9239")

from collections import defaultdict







try:
    path = "profile_4555.csv"

    with open(path, "wb") as f:
        f.write(b"image data here 9239")

    from collections import defaultdict

    def open_picture(profile_path):
        try:
            return open(profile_path, "a+b")
        except OSError:
            print(f"Failed to open path {profile_path}")
            raise

    # assign path to pictures set with defaultdict collection
    pictures = defaultdict(open_picture)
    # assign path to handle
    handle = pictures[path]
    # point at begin of referenced data
    handle.seek(0)
    # assign data to image_data
    image_data = handle.read()
except:
    logging.exception("Expected")
else:
    assert False

##--------------------------
from collections import defaultdict

def open_picture(profile_path):
    try:
        return open(profile_path, "a+b")
    except OSError:
        print(f"Failed to open path {profile_path}")
        raise

# assign path to pictures set with defaultdict collection
pictures = defaultdict(open_picture)
# assign path to handle
handle = pictures[path]

# Example 5
path = "account_9090.csv"

with open(path, "wb") as f:
    f.write(b"image data here 9090")


def open_picture(profile_path):
    try:
        return open(profile_path, "a+b")#test if opens path
    except OSError:
        print(f"Failed to open path {profile_path}")
        raise


class Pictures(dict):
    def __missing__(self, key):
        value = open_picture(key)#if opens assign value to var
        #self[key] = value
        self[key] = value #if commented out still works but pictures is empty dict
        return value


# use the __missing__ function in class Pictures to assign new path
pictures = Pictures()#assign key/value of file to dict
# assign path to handle
handle = pictures[path]#assign value of kety/value from class Pictures ->handle: BinaryIO | None = pictures.get(path)
# point to begin of referenced data
handle.seek(0)
# assing data to image_data
image_data = handle.read()
print(pictures)#{'account_9090.csv': <_io.BufferedRandom name='account_9090.csv'>}
print(image_data)#b'image data here 9090'
