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


result = {}#init result as dict
for name in order:
    # get defaults to 0 if no values are specified
    count = stock.get(name, 0)
    #print(count)
    # get defaults to 8 if no values are specified
    batches = get_batches(count, 8)#size ->8
    print(batches)
    # if batches is True, then add to result dict key/value => name: batches
    if batches:#batches >0 ->true then add new key/value to dict
        result[name] = batches

print(result)


# Example 2
# found is a set with comprehension cerate a dict name: batches
# use function get_batches if name not in stock get defaults to 0
# if name in list order then use function get_batches again to get existing batches

# order = ["screws", "wingnuts", "clips"]
found = {#dict comprehension create stucture name/size pair as expression filled by for loop over order by name present in stock
    name: get_batches(stock.get(name, 0), 8)#expression part
    for name in order
    if get_batches(stock.get(name, 0), 8)
}
print(found)


# Example 3
# create has_bag set see "found" set but now for batches of 4 instead of 8
has_bug = {
    name: get_batches(stock.get(name, 0), 4)#all element with size 4
    for name in order
    if get_batches(stock.get(name, 0), 8)#select just the ones with size 8 so found within has_bags
}

print("Expected:", found)
print("Found:   ", has_bug)


# Example 4
# use ":=" for assigning value/batches if name is in order
# get default 0 if the name is not in stock returns false else True if in stock
# then found is set {name: batches}
found = {#dict with str/int pair as expression and for loop over list to get elements 
    name: batches #expression
    for name in order 
    if (batches := get_batches(stock.get(name, 0), 8))#assign return of finc to var with ":="
}
assert found == {"screws": 4, "wingnuts": 1}
print(found)


# Example 5
try:
    # test for names in stock where count//10 > 0
    # create new variable "tenth" assign if name/size pair in stock > 10 then True
    # add to result {name: size/10 >0}
    # bring assign to if block if referencing "tenth" variable later in comprehension
    result = {
        name: (tenth := count // 10) #cut of divide by 10 assign to var as expression for dict comprehension
        for name, count in stock.items() 
        if tenth > 0 #use calculated value ftom str/int pair to filter
    }
except:
    logging.exception("Expected")
else:
    assert False  # True then return is empty set
    print(result)
    print(tenth)


# Example 6
# sort of initialize "tenth" later assign in if block
result = {
    name: tenth #str/int pair in dict as expression in dict comprehension
    for name, count in stock.items() #for loop over dict
    if (tenth := count // 10) > 0}#calculated and assign and filter in one go
print(result)


# Example 7
# create list determine division 2 assign to "last" variable
# loops over values in stock
half = [
    (last := count // 2) #assign calculated value to var in expression for list comprehension
    for count in stock.values()#for loop over values of name/value pairs in dict
    ]
print(f"Last item of {half} is {last}")


# Example 8
# leak means variable in expression leaks in the loop else better to have
# error=> variable unknown to loop
for count in stock.values():  # Leaks loop variable loop till last then print
    pass
print(f"Last item of {list(stock.values())} is {count}")


# Example 9
# here "count" is not in the same scope as half no leaking of count variable
try:
    del count#del var
    half = [
        count // 2 #expression with count as index in comprehension only ->del in outer scope
        for count in stock.values()
        ]
    print(half)  # Works
    print(count)  # Exception because loop variable didn't leak
                    #NameError: name 'count' is not defined 
except:
    logging.exception("Expected")
else:
    assert False


# Example 10
# see assign values to "batches" in if block return tuple with next statement
# as iterator over "found" tuple
found = (
    (name, batches) #expression str/int tuple in tuple comprehension
    for name in order #for loop over list 
    if (batches := get_batches(stock.get(name, 0), 8))#assign value to var for str/int tuple
)

print(next(found))#next needed for next item by generator
print(next(found))#other next needed for other next item by generator
