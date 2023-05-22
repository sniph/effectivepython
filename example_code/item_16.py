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
    count = counters[key]#set count to last value in dict
else: #if new then value to 1
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
    count = counters[key]#if in dict then true and last value + 1
except KeyError:#if new raise error value = 1
    count = 0

counters[key] = count + 1

print(counters)


# Example 4
key = "multigrain"
# (get method)Return the value for key if
# key is in the dictionary, else default = 0
# assign if key exits else assign 0 then add key,value to set
count = counters.get(key, 0)#assign last value from dict else default 0
counters[key] = count + 1# add 1 to value or assign 1 to new

print(counters)


# Example 5
key = "baguette"

# test key not in set then add key with 0 value
# then update key with 1
if key not in counters:#assign 0 with if to new value 0
    counters[key] = 0#palced in dict with value 0
counters[key] += 1 # add 1 to key/value pair

print(counters)

key = "ciabatta"
# update key with 1 if already in set
# add new key wit value 1
if key in counters:#if in dict +1 else new =1
    counters[key] += 1
else:
    counters[key] = 1

print(counters)

key = "ciabattan"
# try key in set update with 1
# keyerror add new key with value 1
try:
    counters[key] += 1#if in dict +1
except KeyError: #not in dict =1
    counters[key] = 1

print(counters)


# Example 6
votes = {#dict with key/list pairs as build by structure
    "baguette": ["Bob", "Alice"],
    "ciabatta": ["Coco", "Deb"],
}
print(votes)

key = "brioche"
who = "Elmer"


if key in votes:#if key true set value to var
    names = votes[key]
else:
    # connect the key in votes to his list which is called names
    # actually a dict where names is alist connect to key
    votes[key] = names = [] #set item to dict and assign empty list(indirect through var)

print(votes)#with empty list for new key
print(votes[key]) #new key has empty list
print(key)# returns new key
print(names)#returns new value
# append "Elmer" to reference names of "Brioche" is a list
names.append(who) #assign value to empty list named names connected with new dict item
print(names)
print(votes)


# Example 7
key = "rye"
who = "Felix"

try:
    # check "rye" in votes if not make reference and []
    names = votes[key]#if true set dict element to names list
except KeyError:#if new key then set dict element to key/names = [] pair
    votes[key] = names = []

# then append "Felix" to "rye" or [] referenced by names to "rye"
names.append(who)#assign value to new key/names = [] list or existing key/list pair

print(votes)


# Example 8
key = "wheat"
who = "Gertrude"

# assign list to names if not then assign None is default for get method
names = votes.get(key)#if key exists then else None
print(names)
# test names on None (default return from get method)
if names is None:#test for None -> new value
    votes[key] = names = [] #assign empty list to new key/names pair

names.append(who)#assign value to key/list pair

print(votes)


# Example 9
key = "brioche"
who = "Hugh"

# assign key to names in if statement and test on None
# default for get method if not assign []
if (names := votes.get(key)) is None:#assign and test for new in one go
    votes[key] = names = [] #assign [] to new key/list pair

# assign value to key in key/value pair
names.append(who)#general assign key/list pair

print(votes)


# Example 10
key = "cornbread"
who = "Kirk"

# assign list with key to names if not default to []
names = votes.setdefault(key, [])#test for key set existing value to list if new key default to [] list
# assign value to list, in key/list pair
print(votes)#key/list ->empty for new key/list pair
names.append(who)#assign value to key/list pair

print(votes)


# Example 11
data = {}
key = "foo"
value = []
# assign a list(object) to a key or default value/list
data.setdefault(key, value)#create dict with key/list pair
print("Before:", data)
value.append("hello")#add to key/list pair
print("After: ", data)


# Example 12
key = "dutch crunch"
# can also assign default value to key in key,value pair
print(counters)
count = counters.setdefault(key, 0)#set var count to value or default to 0 and assigns new key/value =0 pair to dict
print(counters)
print(count)
# add value to key,value pair
counters[key] = count + 1 #general add 1 to key/value pair 

print(counters)
