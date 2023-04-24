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
names = ["Cecilia", "Lise", "Marie"]
# list comprhension with lengt of names
counts = [len(n) for n in names] #returns a list with the different lengths
print(counts)


# Example 2
longest_name = None
max_count = 0

for i in range(len(names)):
    # range 0,1,2 => 3 names
    # count with indiv. length of names
    count = counts[i]
    # compare indiv.length of names with max
    if count > max_count:#test on longest name save in max_count to retrieve
                            
        longest_name = names[i]
        max_count = count

print(longest_name)


# Example 3
longest_name = None
max_count = 0
# enumerate has inex and name has default
# don't have to use length
for i, name in enumerate(names):#loop with enumerate also auto index
    # get the lengths of the names
    count = counts[i] #auto index for place in list
    if count > max_count: #get right name =>if is true
        longest_name = name
        max_count = count
assert longest_name == "Cecilia"
print(longest_name)


# Example 4
    """_
    This code appears to be written in Python and it assigns a value of
    None to the variable longest_name and a value of 0 to the variable 
    max_count. It then loops over two lists (names and counts) using the 
    zip() function to combine them into pairs of (name, count). For each 
    pair, it checks if the count is greater than the current maximum count. 
    If it is, it updates the value of longest_name to be the current name 
    and updates the value of max_count to be the current count. Finally, 
    it prints out the value of longest_name, which should be "Cecilia" if 
    this code is working correctly.
    """


longest_name = None
max_count = 0
# unpack the zip over names,counts to name,count
# combine lengh,name in one command zip
#counts = [len(n) for n in names] #returns a list with the different lengths
for name, count in zip(names, counts):
    print(names,counts)
    if count > max_count:
        longest_name = name
        max_count = count
assert longest_name == "Cecilia"
print(longest_name)


# Example 5
names.append("Rosalind")
# combine two lists to one list as long as the shortest list
for name, count in zip(names, counts):#default is combine 2 lists max is shortest
    print(names,counts)
    print(name)


# Example 6
import itertools

# to combine lists to longest list use itertools zip_longest
for name, count in itertools.zip_longest(names, counts):#see example 1 now longest list combine with shortest list else None
    print(f"{name}: {count}")
    print(name, count)
