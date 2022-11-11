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
import itertools


# Example 2
# itertools creates iterator => one list out of multiple lists
it = itertools.chain([1, 2, 3], [4, 5, 6])
print(list(it))


# Example 3
# repeats 3 times "hello"string
it = itertools.repeat("hello", 3)
print(list(it))


# Example 4
# calls next 10 times on iterator use the list to cycle over till 10 items
it = itertools.cycle([1, 2])
result = [next(it) for _ in range(10)]
print(result)


# Example 5
# iterate for creating several list with "list" method on iterator int is 3 cycles/variables
it1, it2, it3 = itertools.tee(["first", "second"], 3)
print(list(it1))
print(list(it2))
print(list(it3))


# Example 6
keys = ["one", "two", "three"]
values = [1, 2]

# zip joins list key/value combinations up to shortest list length => 3 versus 2 gives 2 list of 2 values
normal = list(zip(keys, values))
print("zip:        ", normal)

# zip_longest joins list key/value combinations up to longest list length default for missing values
it = itertools.zip_longest(keys, values, fillvalue="nope")
longest = list(it)
print("zip_longest:", longest)


# Example 7
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# generates slice call with "list" method
first_five = itertools.islice(values, 5)
print("First five: ", list(first_five))

# generates slice call => start,stop,step on values =>with "list" method
middle_odds = itertools.islice(values, 2, 8, 2)
print("Middle odds:", list(middle_odds))


# Example 8
# filter through values with lambda function as argument in generator, call with "list" method
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
less_than_seven = lambda x: x < 7
it = itertools.takewhile(less_than_seven, values)
print(list(it))


# Example 9
# drop/filter out items from list, return leftover with "list" method
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
less_than_seven = lambda x: x < 7
it = itertools.dropwhile(less_than_seven, values)
print(list(it))


# Example 10
# use filter method  to mod 2 items from values
# list method as iterator over filter result
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = lambda x: x % 2 == 0

filter_result = filter(evens, values)
print(filter_result)
print("Filter:      ", list(filter_result))

# filterfalse method of itertools as complement of filter method
filter_false_result = itertools.filterfalse(evens, values)
print("Filter false:", list(filter_false_result))


# Example 11
# method accumulate of itertools adds up progressive
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sum_reduce = itertools.accumulate(values)
print("Sum:   ", list(sum_reduce))

# take n ste + n st + 1 value then the mod 20
def sum_modulo_20(first, second):
    output = first + second
    return output % 20


# function takes cum values n and (n+1) them mod 20
modulo_reduce = itertools.accumulate(values, sum_modulo_20)
print("Modulo:", list(modulo_reduce))


# Example 12
# is product 2x2 combinations
# like this [(1, 1), (1, 2), (2, 1), (2, 2)]
single = itertools.product([1, 2], repeat=2)
single2 = itertools.product([1, 2], [1, 2])  # same as repeat 2
print("Single:  ", list(single))
print("single  2", list(single2))

# product of two list a 2x2 lis by iterator list function
multiple = itertools.product([1, 2], ["a", "b"])
print("Multiple:", list(multiple))


# Example 13
# combinations with other values except hisself with list function position is important
it = itertools.permutations([1, 2, 3, 4], 2)
original_print = print
print = pprint
print(list(it))
print = original_print


# Example 14
# combinations with other values except hisself with list function position is not important
# take values out of list
it = itertools.combinations([1, 2, 3, 4], 2)
print(list(it))


# Example 15
# all combinations possible with full list
it = itertools.combinations_with_replacement([1, 2, 3, 4], 2)
original_print = print
print = pprint
print(list(it))
print = original_print
