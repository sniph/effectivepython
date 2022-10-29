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
counters = {
    "pumpernickel": 2,
    "sourdough": 1,
}


# Example 2
key = "wheat"

# if key in counters then then update dist else add
# key with value 1
if key in counters:
    count = counters[key]
else:
    count = 0

counters[key] = count + 1

# counters[key]
print(counters["pumpernickel"])

print(counters)


# Example 3
key = "brioche"

# use of try if not in set then raise keyerror
# set count = 0 and add new key with value 1 to set
try:
    count = counters[key]
except KeyError:
    count = 0

counters[key] = count + 1

print(counters)


# Example 4
key = "multigrain"
# (get method)Return the value for key if
# key is in the dictionary, else default = 0
# assign if key exits else assign 0 then add key,value to set
count = counters.get(key, 0)
counters[key] = count + 1

print(counters)


# Example 5
key = "baguette"

# test key not in set then add key with 0 value
# then update key with 1
if key not in counters:
    counters[key] = 0
counters[key] += 1

print(counters)

key = "ciabatta"
# update key with 1 if already in set
# add new key wit value 1
if key in counters:
    counters[key] += 1
else:
    counters[key] = 1

print(counters)

key = "ciabattan"
# try key in set update with 1
# keyerror add new key with value 1
try:
    counters[key] += 1
except KeyError:
    counters[key] = 1

print(counters)


# Example 6
votes = {
    "baguette": ["Bob", "Alice"],
    "ciabatta": ["Coco", "Deb"],
}
print(votes)

key = "brioche"
who = "Elmer"


if key in votes:
    names = votes[key]
else:
    # connect the key in votes to his list which is called names
    # actually a dict where names is alist connect to key
    votes[key] = names = []

print(votes)
print(votes[key])
print(names)
# append "Elmer" to reference names of "Brioche" is a list
names.append(who)
print(names)
print(votes)


# Example 7
key = "rye"
who = "Felix"

try:
    # check "rye" in votes if not make reference and []
    names = votes[key]
except KeyError:
    votes[key] = names = []

# then append "Felix" to "rye" or [] referenced by names to "rye"
names.append(who)

print(votes)


# Example 8
key = "wheat"
who = "Gertrude"

# assign list to names if not then assign None is default for get method
names = votes.get(key)
print(names)
# test names on None (default return from get method)
if names is None:
    votes[key] = names = []

names.append(who)

print(votes)


# Example 9
key = "brioche"
who = "Hugh"

# assign key to names in if statement and test on None
# default for get method if not assign []
if (names := votes.get(key)) is None:
    votes[key] = names = []

# assign value to key in key/value pair
names.append(who)

print(votes)


# Example 10
key = "cornbread"
who = "Kirk"

# assign list with key to names if not default to []
names = votes.setdefault(key, [])
# assign value to list, in key/list pair
names.append(who)

print(votes)


# Example 11
data = {}
key = "foo"
value = []
# assign a list(object) to a key or default value/list
data.setdefault(key, value)
print("Before:", data)
value.append("hello")
print("After: ", data)


# Example 12
key = "dutch crunch"
# can also assign default value to key in key,value pair
count = counters.setdefault(key, 0)
print(count)
# add value to key,value pair
counters[key] = count + 1

print(counters)
