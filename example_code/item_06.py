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
from re import A

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
snack_calories = {
    "chips": 140,
    "popcorn": 80,
    "nuts": 190,
}
print(snack_calories
      )#print the set as key values
items = tuple(snack_calories.items())#convert to tuple of tuples from set
print(items)


# Example 2
item = ("Peanut butter", "Jelly")
first = item[0] #get items wit [] notation
second = item[1]
print(first, "and", second)


# Example 3
try:
    pair = ("Chocolate", "Peanut butter")
    pair[0] = "Honey"
# pair[0] = pair[1]
except:
    logging.exception("Expected")
else:
    assert False
print(pair[0])#cannot assign new element with pair[0] = "Honey" in existing tuple


# Example 4
item = ("Peanut butter", "Jelly")
first, second = item  # Unpacking positional ordering
print(first, "and", second) 


# Example 5
favorite_snacks = {#set dict as key tuple combination
    "salty": ("pretzels", 100),
    "sweet": ("cookies", 180),
    "veggie": ("carrots", 20),
}

(#assign every element from positional to var
    (type1, (name1, cals1)),
    (type2, (name2, cals2)),
    (type3, (name3, cals3)),
) = favorite_snacks.items()

print(f"Favorite {type1} is {name1} with {cals1} calories")#use values as vars in string with {} and vars
print(f"Favorite {type2} is {name2} with {cals2} calories")
print(f"Favorite {type3} is {name3} with {cals3} calories")


# Example 6
def bubble_sort(a):
    for _ in range(len(a)):
        # repeat for every item in list
        for i in range(1, len(a)):
            # move element 1  to right pos in list
            if a[i] < a[i - 1]:#change order in list on first letter basis
                temp = a[i]
                a[i] = a[i - 1]
                a[i - 1] = temp

print("pretzels"<"xarrotsxxx") #true compare firts letter in stings
names = ["pretzels", "carrots", "arugula", "bacon"]
for _ in range(len(names)):#get length of list and range over
    print(_)
    print(names[_])

bubble_sort(names)#call function to reorder on first letter
print(names)


# Example 7
def bubble_sort(a):
    for _ in range(len(a)):
        for i in range(1, len(a)):#get second element to last

            if a[i] < a[i - 1]: #compare second with first element
                a[i - 1], a[i] = a[i], a[i - 1]  # Swap elements assign positional for '=' to after '='


a = ["pretzels", "carrots", "arugula", "bacon"]
for _ in range(len(a)): #a is local to function but references the list assigned and changes the values => a and names reference the same list
    for i in range(1, len(a)):

        if a[i] < a[i - 1]:
            a[i - 1], a[i] = a[i], a[i - 1]
print(a)#order is not change list a immutable


names = ["pretzels", "carrots", "arugula", "bacon"]
bubble_sort(names)#use function to change order of list, 
                    #referencing list names in function will change the list because the list names is used
print(names)


# Example 8
snacks = [("bacon", 350), ("donut", 240), ("muffin", 490)]
for i in range(len(snacks)):#show numbering of items in list
    item = snacks[i] #iterate over list snacks
    name = item[0] #return first part eq name of every iteration of snack
    calories = item[1] # return second part eq calories of every iteration
    # have to create index i+1 i starts with 0
    print(f"#{i+1}: {name} has {calories} calories")


# Example 9
for rank, (name, calories) in enumerate(snacks, 1):#numbering without for loop with enumerate starts with first item with rank as auto index
    # unpacking and index in one line
    print(f"#{rank}: {name} has {calories} calories")
