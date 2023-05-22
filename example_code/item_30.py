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

# here are the example files stored
TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

# Make sure Windows processes exit cleanly
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
# Change the current working directory to the specified path.
os.chdir(TEST_DIR.name)


def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()


atexit.register(close_open_files)


# Example 1
# enumerate generate index,item pair use generator like list
# "result" looks for index number of " " characters in address string
def index_words(text):
    result = []#create list as bucket
    # if there is text append first item append(0) then index + 1
    if text:#test on text
        result.append(0)#assign "0" to list
    for index, letter in enumerate(text):#loop over text number every character even space
        if letter == " ":#filter for space then append value of first letter of next word to list
            result.append(index + 1)
    return result

 

# Example 2
address = "Four score and seven years ago..."
address1 = "Four score and seven years ago our fathers brought forth on this continent a new nation, conceived in liberty, and dedicated to the proposition that all men are created equal."
# generate index/value pairs list
print(index_words(address))

a = list(enumerate(address))#number all characters in string
print(a)

result = index_words(address)
# print all
print(result)#[0, 5, 11, 15, 21, 27]
# first 10 reults
print(result[:4])#first 4 results -> [0, 5, 11, 15]


# Example 3
# if text then append text 0 to list else if letter = " " append index + 1
# "next" statement returns following value
def index_words_iter(text):#(function) def index_words_iter(text: Any) -> Generator[int, Any, None]
    if text:
        yield 0
    for index, letter in enumerate(text):#loop over text with enumerate to create indexed elements
        if letter == " ":
            yield index + 1


# Example 4
# "it" object to use for iterator next/lsit method
it = index_words_iter(address)#generator to be next over to get every next element

print(it)#<generator object index_words_iter at 0x000001D89FF5C430>
print(next(it))#next get element and remove from generator object
print(next(it))
print(list(it))#list method returns the last status of it after the next methods

# Example 5
# "list" method generates list over the enumerate yields for every item in address
result = list(index_words_iter(address))
print(result[:10])


# Example 6


def index_file(handle):#peel the structure from line to word to letter
    # initialize the offset of the file
    offset = 0
    for line in handle:#loop over lines in file
        # if there is a line true
        if line:#first line return offset index
            # return value offset
            yield offset
        # loop over lines
        for letter in line:#loop over characters in line and number with offset index
            # for every letter and ! to "offset" variable
            offset += 1
            # if letter is space then return offset number
            if letter == " ":# filter on space then return the offset index
                yield offset


# Example 7
address_lines = """Four  score and seven years
ago our fathers brought forth on this
continent a new nation, conceived in liberty,
and dedicated to the proposition that all men
are created equal."""
# here are the example files stored
# TEST_DIR = tempfile.TemporaryDirectory()
#'C:\\Users\\HARRYS~1\\AppData\\Local\\Temp\\2\\tmphvfh2fyp'>
with open("address.txt", "w") as f:#write text to file
    f.write(address_lines)

import itertools

# read the file to f:
with open("address.txt", "r") as f:#read file content and assign to var
    # assign data to "it" variable pass through index_file function
    it = index_file(f)
    # get the first 10 items from "it" variable with islice
    results = itertools.islice(it, 0, 10)#use islice to get part of generator object elements to var results
    # use "list" method to generate a list of results object
    print(list(results))#use list method to unpack generator as list
