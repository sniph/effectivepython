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
from unittest import result

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
# get total and assign individual percentages to "result" list
def normalize(numbers):
    total = sum(numbers)
    result = []#init list by structure
    for value in numbers:#loop over numbers
        percent = 100 * value / total#get percentage part of every element in list
        result.append(percent)#add to list by append method
    return result


# Example 2
# use "visits" list in function to assign items to "percent" list
visits = [15, 35, 80]
percentages = normalize(visits)#get percentual part of element of list
print(percentages)
assert sum(percentages) == 100.0


# Example 3
# write number in for loop to file through handele "f"
#'C:\\Users\\HARRYS~1\\AppData\\Local\\Temp\\2\\tmp150p0xke'>
path = "my_numbers.txt"
with open(path, "w") as f:
    for i in (15, 35, 80):
        f.write("%d\n" % i)

# read file.txt through function and return number list
def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)


# Example 4
# assigndata to "it" list
it = read_visits("my_numbers.txt")
#print(list(it))
# assign the percentages calculated from "ït" list
percentages = normalize(list(it))#use list method else [] generator versus list in func
print(percentages)


# Example 5
# go over "it" generator object with "list" method
# second call generates []
it = read_visits("my_numbers.txt")
print(list(it))#list method on generator once
print(list(it))  # Already exhausted in second call of list method


# Example 6
# assign "numbers" under "list" method to  "numbers_copy" list
# assign calculated percentages to "results" list
def normalize_copy(numbers):
    numbers_copy = list(numbers)  # Copy the iterator from generator to list object concert input to list
    total = sum(numbers_copy)
    result = []
    for value in numbers_copy:
        percent = 100 * value / total
        result.append(percent)
    return result


# Example 7
# run multiple times with same outcome "list" methode on generator now short-cuts to new list
it = read_visits("my_numbers.txt")
percentages = normalize_copy(it)#get list from func and assign to var list
print(percentages)
assert sum(percentages) == 100.0


# Example 8
# get the data through call function "read_visits" with lambda as argument
# in "normalize_func" function
def normalize_func(get_iter):
    # call data enew with lambda as argument =>get_iter()
    total = sum(get_iter())  # New iterator
    result = []#init list
    # call data again for the loop iteration and create "result" list
    for value in get_iter():  # New iterator -> loop over anon func as generator
        percent = 100 * value / total
        result.append(percent)#add to list
    return result


# Example 9
# feed argument as lambda function on path
path = "my_numbers.txt"
percentages = normalize_func(lambda: read_visits(path))#input anon func to get file and content then func to get list
print(percentages)
assert sum(percentages) == 100.0


# Example 10
# create class for setup generator iter to process lines when called bij iterator


class ReadVisits:#return will be generator see iter part
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):#create generator over data in file
        with open(self.data_path) as f:
            for line in f: #loop over lines in file
                yield int(line)#convert str to int


def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


# Example 11
# initilize instance of "ReadVisits" class with "path" argument
# read in the data from path/file in "visits" variable
visits = ReadVisits(path)#create new class -> <__main__.ReadVisits object at 0x000001D89FF82980>
print(visits)
percentages = normalize(visits)#generator as input then append to list
print(percentages)
assert sum(percentages) == 100.0


# Example 12
#"is" test if "numbers" argument is an iter identity if same object
#container type can be used multiple times instead of iter type
def normalize_defensive(numbers):
    if iter(numbers) is numbers:  # An iterator -- bad! 
        raise TypeError("Must supply a container")
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

#call "normalize_defensive" function to test for iter or container
visits = [15, 35, 80]
normalize_defensive(visits)  # No error can iter over list return also list

#now "it" as argument is passed as iter
#it: <list_iterator object at 0x000001389244D840>

it = iter(visits)
try:
    #will generate false feed is iterator need container like list
    normalize_defensive(it)
except TypeError:#TypeError: Must supply a container so get passed
    pass
else:
    assert False


# Example 13
from collections.abc import Iterator

#same test on iter is done in normalize_defensive with module "Iterator"
def normalize_defensive(numbers):
    if isinstance(numbers, Iterator):  # Another way to check
        raise TypeError("Must supply a container")
    total = sum(numbers)
    result = []
    for value in numbers:#loop over list is option
        percent = 100 * value / total
        result.append(percent)
    return result

#this works feed container
visits = [15, 35, 80]
normalize_defensive(visits)  # No error list is iterable

#this not feed is iter
it = iter(visits)#<list_iterator object at 0x000001D89FF835B0>
print(list(it))
try:
    normalize_defensive(list(it))#makes list from iterable
except TypeError:#TypeError: Must supply a container
    pass
else:
    assert False#AssertionError because its True iterator-iterable-list


# Example 14
#feed is container pass test for iter
visits = [15, 35, 80]
percentages = normalize_defensive(visits)#list as input
assert sum(percentages) == 100.0

#feed is containre pass test for iter
visits = ReadVisits(path)
percentages = normalize_defensive(visits)#or genarator as input
assert sum(percentages) == 100.0


# Example 15
#feed fails pass iter to "normalize_defensive" function
try:
    visits = [15, 35, 80]
    it = iter(visits)#is iterator should list or generator
    normalize_defensive(it)#TypeError: Must supply a container
except:
    logging.exception("Expected")
else:
    assert False
