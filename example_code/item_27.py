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
# classic way to add numbers to new list from list with processing
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = []
for x in a:#basic assign elements from list to no list under operation x^2
    squares.append(x**2)
print(squares)


# Example 2
squares = [x**2 for x in a]  # List comprehension all operations in the list
print(squares)


# Example 3
alt = map(lambda x: x**2, a)#define anon func(x) x^2 on list return new list
#print(list(alt)) #[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
assert list(alt) == squares, f"{alt} {squares}"


# Example 4
# list comprehension the code inside the list
even_squares = [x**2 for x in a if x % 2 == 0]  # use of squared and mod 2 process inside list
print(even_squares)#[4, 16, 36, 64, 100]

# Example 5
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
alt = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))#filter outcome anon func on dividable by 2
#print(list(alt)) #[4, 16, 36, 64, 100]
#print(list(alt))#returns [] the alt map seems to be empty after firts list invocation in print
assert even_squares == list(alt)#if print before assert

# need of list to generate the squares as comprhension gives object id
alt2 = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, a)))
print(list(alt2)) #[4, 16, 36, 64, 100]
# gives object id in list format
alt3 = [map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))]
print(alt3)#see the kind of object passed


# Example 6
# create dict for every number key/value pair number: squared
# as set comprehension
even_squares_dict = {x: x**2 for x in a if x % 2 == 0}#create dict by structure use x^2 then filter dividable by 2
threes_cubed_set = {x**3 for x in a if x % 3 == 0}#use x^3 then filter dividable by 3
print(even_squares_dict)
print(threes_cubed_set)


# Example 7
# generate dictionary with dict function key/value pairs number: square
alt_dict = dict(map(lambda x: (x, x**2), filter(lambda x: x % 2 == 0, a)))#create dict element/element^2 pair filter on dividable by 2
print(alt_dict)
# generate set with set function number cubed as in list a mod 3 =>3 6 9 not sorted
alt_set = set(map(lambda x: x**3, filter(lambda x: x % 3 == 0, a)))#create set with unique element^3  filter on dividable by 3
print(alt_set)
assert even_squares_dict == alt_dict
assert threes_cubed_set == alt_set
