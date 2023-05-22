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
import random

# 10 times create lines with random numbers(0-100) times 'a'
# C:\Users\HarrySnippe\AppData\Local\Temp\2\tmpqsgv3sqc =>see TESTDIR
# tmpqsgv3sqc start script
with open("my_file.txt", "w") as f:
    for _ in range(10):#loop 10 times
        f.write("a" * random.randint(0, 100))#write multiple "a" times random 0-100
        f.write("\n")#then newline

# use list comprehension to calculate length of lines in file
value = [len(x) #expression length line
         for x in open("my_file.txt")] #loop over lines in file
print(value)


# Example 2
# "it" varaible as generator object
it = (len(x) #create tuple for length of lines
      for x in open("my_file.txt"))
print(it)#generator object
#print(tuple(it))#generator object needs tuple method to create tuple takes all values in one go else next method


# Example 3
# "next " method process all the data from file ones the
# Traceback (most recent call last):
# File "<stdin>", line 1, in <module>
# StopIteration
print(next(it))#take first item from tuple
print(next(it))#take next item from tuple


# Example 4
# generator object roots created in tuple form
roots = ((x, x**0.5) 
         for x in it)
print(roots)#again generator object in tuple form

# Example 5
# next will generate till end file even if generator object is "root" instead of "it"
# or the file as to be generated again to get all values for processing with next calls
# A Python generator is:
"""
    a Python function or method
    which acts as an iterator
    which keeps track of when it's called (stateful)
    and returns data to its caller using the yield keyword
"""

print(next(roots))#get first item of generator object use tuple method for all items
