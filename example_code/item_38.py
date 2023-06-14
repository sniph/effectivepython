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
names = ['Socrates', 'Archimedes', 'Plato', 'Aristotle']
names.sort(key=len)#sort will mutate list
print(names)


# Example 2
def log_missing():
    print('Key added')
    return 0

print(log_missing())#invoke func with print and return
# Example 3
from collections import defaultdict

current = {'green': 12, 'blue': 3}#create key/int dict
increments = [#create list of tuples
    ('red', 5),
    ('blue', 17),
    ('orange', 9),
]
result = defaultdict(log_missing, current)#use of log  func unclear
print('Before:', dict(result))
for key, amount in increments:#loop over list of tuples add to dict key/int pairs and update int
    result[key] += amount
print('After: ', dict(result))


# Example 4
def increment_with_report(current, increments):#func on dict at list of tuples
    added_count = 0#init var

    def missing():
        nonlocal added_count  # Stateful closure as global var -> outside func
        added_count += 1
        return 0

    result = defaultdict(missing, current)#calls missing func for item not in dict
    for key, amount in increments:
        result[key] += amount

    return result, added_count


# Example 5
result, count = increment_with_report(current, increments)
assert count == 2#called for missing item in dict
print(count)
print(result)


# Example 6
class CountMissing:
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0


# Example 7
counter = CountMissing()#initiate new class to create counter
result = defaultdict(counter.missing, current)  # Method ref use start value for new items in dict
for key, amount in increments:
    result[key] += amount
assert counter.added == 2
print(counter.added)
print(result)


# Example 8
class BetterCountMissing:
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0

counter = BetterCountMissing()
assert counter() == 0
assert callable(counter)


# Example 9
counter = BetterCountMissing()#initiate new class counter
result = defaultdict(counter, current)  # Relies on __call__ use start value add count new items in default dict
for key, amount in increments:
    result[key] += amount
assert counter.added == 2
print(result)
