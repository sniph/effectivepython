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
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)


def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()


atexit.register(close_open_files)


# Example 1
from urllib.parse import parse_qs

my_values = parse_qs("red=5&blue=0&green=", keep_blank_values=True)#returns set of  key/value pair with value between []
print(my_values)
print(repr(my_values))


# Example 2
print("Red:     ", my_values.get("red"))#return value from set by key
print("Green:   ", my_values.get("green"))
print("Opacity: ", my_values.get("opacity"))


# Example 3
# For query string 'red=5&blue=0&green='
red = my_values.get("red", [""])[0] or 0 #take first element with get from dict filter on red or 0 return string or 0
green = my_values.get("green", [""])[0] or 0
opacity = my_values.get("opacity", [""])[0] or 0
print(f"Red:     {red!r}")#or is used to call repr method on value
print(f"Green:   {green!r}")
print(f"Opacity: {opacity!r}")


# Example 4
red = int(my_values.get("red", [""])[0] or 0)#make int from string or 0
green = int(my_values.get("green", [""])[0] or 0)
opacity = int(my_values.get("opacity", [""])[0] or 0)
print(f"Red:     {red!r}")
print(f"Green:   {green!r}")
print(f"Opacity: {opacity!r}")


# Example 5
red_str = my_values.get("red", [""]) #get value for key else empty list
red = int(red_str[0]) if red_str[0] else 0 #test on empty lsit then 0
green_str = my_values.get("green", [""])
green = int(green_str[0]) if green_str[0] else 0
opacity_str = my_values.get("opacity", [""])
opacity = int(opacity_str[0]) if opacity_str[0] else 0
print(red_str)
print(green_str)
print(opacity_str)

print(f"Red:     {red!r}")
print(f"Green:   {green!r}")
print(f"Opacity: {opacity!r}")


# Example 6
green_str = my_values.get("green", [""])
if green_str[0]:#test on empty list
    green = int(green_str[0])
else:
    green = 0
print(f"Green:   {green!r}")


# Example 7
def get_first_int(values, key, default=0):#function return item from dict else default to 0
    found = values.get(key, [""])
    if found[0]:
        return int(found[0])
    return default

# Example 8
green = get_first_int(my_values, "green")#use general function to get value from dict
print(f"Green:   {green!r}")

pictures = {}
path = 'profile_9991.png'

with open(path, 'wb') as f:
    f.write(b'image data here 9991')
#test path in picture then assign path from picture set to handle
if path in pictures:
    handle = pictures[path]
#if not in pictures set then assign open path to handle
else:
    try:
        handle = open(path, 'a+b')
    except OSError:
        print(f'Failed to open path {path}')
        raise
    #assign new handle to pictures set
    else:
        pictures[path] = handle

handle.seek(0)
image_data = handle.read()

print(pictures)
print(image_data)