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
visits = {
    "Mexico": {"Tulum", "Puerto Vallarta"},
    "Japan": {"Hakone"},
}
print(visits)

# Example 2
# assign key set to key if not {} add value to set

visits.setdefault("France", set())#assign set() as key/value -> 'key:set()'
print(visits)
visits.setdefault("France", set()).add("Arles")  # Short replace set() in key/set() pair by add method
print(visits)

# assign value to set of the key else get method defaults to "None"
# test on "None" then assign empty set {}
if (japan := visits.get("Japan")) is None:  # Long look for key in dict with key/set pairs 
    visits["Japan"] = japan = set() #set set() to key/set() pair in dict and assign set() to var japan
print(japan)#var japan 
japan.add("Kyoto")#replace set() in var japan if empty else add to existing element in key/set

# swap print statement with pprint
original_print = print
print = pprint

print(visits)
pprint(visits)
# swap print statement with pprint reverse
print = original_print


# Example 3
# make class with city add method
class Visits:
    def __init__(self):
        self.data = {}#set data to empty set {}

    def add(self, country, city):
        # make key,set combinations within data set
        city_set = self.data.setdefault(country, set())#assign key/set() or existing key/set to dict city_set 
        city_set.add(city)




# Example 4
# initialize visits variable from  class Visits:
visits = Visits()#assign class object to visits
print(visits)
# use add method from class Visits to add cities to countries set
visits.add("Russia", "Yekaterinburg")#use add method from class Visits
visits.add("Tanzania", "Zanzibar")
print(visits.data)#use data method from class Visits


# Example 5
from collections import defaultdict

# default creates default value for every key so every as a value is to add to
class Visits:
    def __init__(self):
        self.data = defaultdict(set)

    def add(self, country, city):
        self.data[country].add(city)


visits = Visits()
print(visits.data)#defaultdict(<class 'set'>, {})
#visits.add("England",set())
print(visits.data)
visits.add("England", "Bath")#assign key/set pair to dict
visits.add("England", "London")#assign set to existing key/set pair ->add method from class Visits needs key/set pair as input
print(visits.data)
