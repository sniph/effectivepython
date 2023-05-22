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
def sort_priority(values, group):

    # "x" new defined in local function helper
    # "group" in outer function defined
    def helper(x):#assign rank to every number to be sorted on
        if x in group:
            return (0, x)
        return (1, x)

    # values defined in function, sorting according to tuples
    # see docstring
    values.sort(key=helper)#key is function to rank in group ->0 else 1
    # print(values.sort(key=helper))
    """#    _summary_docstring
    #see how the helper function classifies the lsit of numbers    
    [helper(x) for x in numbers]
    [(0, 2), (0, 3), (0, 5), (0, 7), (1, 1), (1, 4), (1, 6), (1, 8)]

        """


# Example 2
#
# use sort_priority function to arrange numbers in list
# sort on tuples in group or not 0 or 1
numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
sort_priority(numbers, group)#rank number if in group first then other
print(numbers)


# Example 3
# found flag has to return if numbers in group are found
# scope of "found" is local to most inner function
# inner fuction is local for outer function so those variables apply
numbers=[]
print(numbers)
def sort_priority2(numbers, group):
    found = False#use found to see scope level

    def helper(x):
        if x in group:
            found = True  # Seems simple found -> False outer function scope
            #found  -> True in inner function scope
            return (0, x)
        return (1, x)

    numbers.sort(key=helper)#numbers list is changed by sort method with key
    # always False helper function doesn't appy to outer function
    return found#doesn't do much settle scope


# Example 4
# test on found with found flag in outer function
numbers = [8, 3, 1, 2, 5, 4, 7, 6]
found = sort_priority2(numbers, group)#call for 
print("Found:", found)
print(numbers)


# Example 5
# variable not defined when try to assign to other variable
try:
    foo = does_not_exist * 5#var is not assigned before multiplication
except:
    logging.exception("Expected")
else:
    assert False


# Example 6
# scope is in different functions the inner cannot change outer scope
def sort_priority2(numbers, group):
    found = False  # Scope: 'sort_priority2'

    def helper(x):
        if x in group:
            found = True  # Scope: 'helper' -- Bad!
            return (0, x)
        return (1, x)

    numbers.sort(key=helper)
    return found


# Example 7


def sort_priority3(numbers, group):
    found = False
    # nonlocal will bring inner scop to nearest outer scope
    # so here the nonlocal inner scope "found" can change the outer scope "found"
    def helper(x):
        nonlocal found  # Added to make found var global overwrite outer found var
        if x in group:
            found = True
            return (0, x)
        return (1, x)

    numbers.sort(key=helper)
    return found#else found ->False with nonlocal found -> True 



# Example 8
# test inner/outer scope with nonlocal variables
# found is now flag for numbers in group as "True"
numbers = [8, 3, 1, 2, 5, 4, 7, 6]
found = sort_priority3(numbers, group)
assert found
print(found)
assert numbers == [2, 3, 5, 7, 1, 4, 6, 8]


# Example 9
numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}


class Sorter:
    def __init__(self, group):#init names of var
        self.group = group #assign var
        self.found = False #assign static bool

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)


# initialize Sorter class with helper function(__call__)
# seems to get "found" in same scope as init function in the class
# nonlocal function can get out of the closure of the function(scope)
sorter = Sorter(group)#init class
numbers.sort(key=sorter)#use method from class as key
assert sorter.found is True#found is set in init and changed in call method same scope
assert numbers == [2, 3, 5, 7, 1, 4, 6, 8]
