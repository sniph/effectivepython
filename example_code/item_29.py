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
stock = {
    "nails": 125,
    "screws": 35,
    "wingnuts": 8,
    "washers": 24,
}

order = ["screws", "wingnuts", "clips"]

# floor division 1,5 =>1
def get_batches(count, size):
    return count // size


result = {}
for name in order:
    # get defaults to 0 if no values are specified
    count = stock.get(name, 0)
    # get defaults to 8 if no values are specified
    batches = get_batches(count, 8)
    # if batches is True, then add to result dict key/value => name: batches
    if batches:
        result[name] = batches

print(result)


# Example 2
# found is a set with comprehension cerate a dict name: batches
# use function get_batches if name not in stock get defaults to 0
# if name in list order then use function get_batches again to get existing batches

# order = ["screws", "wingnuts", "clips"]
found = {
    name: get_batches(stock.get(name, 0), 8)
    for name in order
    if get_batches(stock.get(name, 0), 8)
}
print(found)


# Example 3
# create has_bag set see "found" set but now for batches of 4 instead of 8
has_bug = {
    name: get_batches(stock.get(name, 0), 4)
    for name in order
    if get_batches(stock.get(name, 0), 8)
}

print("Expected:", found)
print("Found:   ", has_bug)


# Example 4
# use ":=" for assigning value/batches if name is in order
# get default 0 if the name is not in stock returns false else True if in stock
# then found is set {name: batches}
found = {
    name: batches for name in order if (batches := get_batches(stock.get(name, 0), 8))
}
assert found == {"screws": 4, "wingnuts": 1}


# Example 5
try:
    # test for names in stock where count//10 > 0
    # create new variable "tenth" assign if name/size pair in stock > 10 then True
    # add to result {name: size/10 >0}
    # bring assign to if block if referencing "tenth" variable later in comprehension
    result = {
        name: (tenth := count // 10) for name, count in stock.items() if tenth > 0
    }
except:
    logging.exception("Expected")
else:
    assert False  # True then return is empty set
    print(result)
    print(tenth)


# Example 6
# sort of initialize "tenth" later assign in if block
result = {name: tenth for name, count in stock.items() if (tenth := count // 10) > 0}
print(result)


# Example 7
# create list determine division 2 assign to "last" variable
# loops over values in stock
half = [(last := count // 2) for count in stock.values()]
print(f"Last item of {half} is {last}")


# Example 8
# leak means variable in expression leaks in the loop else better to have
# error=> variable unknown to loop
for count in stock.values():  # Leaks loop variable
    pass
print(f"Last item of {list(stock.values())} is {count}")


# Example 9
# here "count" is not in the same scope as half no leaking of count variable
try:
    del count
    half = [count // 2 for count in stock.values()]
    print(half)  # Works
    print(count)  # Exception because loop variable didn't leak
except:
    logging.exception("Expected")
else:
    assert False


# Example 10
# see assign values to "batches" in if block return tuple with next statement
# as iterator over "found" tuple
found = (
    (name, batches) for name in order if (batches := get_batches(stock.get(name, 0), 8))
)

print(next(found))
print(next(found))
