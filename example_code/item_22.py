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
# make log from message and join statement with tuple comprehension
# with no values TypeError missing values
def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ", ".join(str(x) for x in values)
        print(f"{message}: {values_str}")


log("My numbers are", [1, 2])
log("Hi there", [])#test empty list []->False
log("Hi there2")#should 2 args now error

# Example 2
# use " * " before variable to declare variable optional
# no values gives "()" => not () evaluates to true
def log(message, *values):  # The only difference -> values is optional
    if not values:
        print(message)
        print(values)
    else:
        values_str = ", ".join(str(x) for x in values)
        print(f"{message}: {values_str}")


log("My numbers are", 1, 2)
log("Hi there")  # Much better no error *arg makes values optional


# Example 3
# receive list as seperate items after message not as 1 list
favorites = [7, 33, 99]
log("Favorite colors", *favorites)#takes even list values as multiple argument use as seperate item from list
log("Favorite colors", favorites)#now arg is the list as item

# Example 4
def my_generator():
    for i in range(10):
        yield i#optional without works


def my_func(*args):
    print(args)


# with unpack you need a variable and *variable
# this you assign generator to a variable it and print *it
it = my_generator()
print(*it)#print all items by *var
print(it)#print object

# here unpack first then print a,it
a, *it = my_generator()
print([a, it])#prints list with 2items a and list it 

# print trough function double *variable
it = my_generator()#call func return items
my_func(*it)#use items in func 
my_func(it)#gets generator object

# Example 5
def log(sequence, message, *values):
    # when values is empty tuple () => not () is True them no values printed
    if not values:
        print(f"{sequence} - {message}")
    # if values print all
    else:
        values_str = ", ".join(str(x) for x in values)
        print(f"{sequence} - {message} {values_str}") 


log(1, "Favorites", 7, 33)  # New with *args OK "1 - Favorites 7, 33"
log(1, "Hi there")  # New message only OK "1 - Hi there"
log("Favorite numbers", 7, 33)  # Old usage breaks#now value message can be the first number "Favorite numbers - 7 33"
