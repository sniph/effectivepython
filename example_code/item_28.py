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
# list in list comprehension possible double for loop
# first smallest item x in row, then row in matrix to peel off structure
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
print(flat)


# Example 2
# change the matrix first x in row then row in matrix
# insert comprehnsion for list on row level then adopt for matrix as row

squared = [[x**2 for x in row] for row in matrix]
print(squared)


# Example 3
# unpack first x in row, row in matrix, matrix in complete_lsit
# to flatten the structure into one list
my_lists = [
    [[1, 2, 3], [4, 5, 6]],
    [[7, 8, 9], [10, 11, 12]],
]
flat = [x for sublist1 in my_lists for sublist2 in sublist1 for x in sublist2]
print(flat)


# Example 4
# the convetional way to unpack matrix structure to list by for loops
# from meta to detail as loop over lower order to higher level
flat = []
for sublist1 in my_lists:
    for sublist2 in sublist1:
        flat.extend(sublist2)
print(flat)


# Example 5
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# comprehension with double if's x>4 (unspoken and)mod 2
b = [x for x in a if x > 4 if x % 2 == 0]
# comprehension with  if and expressed "and"
c = [x for x in a if x > 4 and x % 2 == 0]
print(b)
print(c)
assert b and c
print(b and c)
assert b == c
print(b == c)

# Example 6
# if's on x in row and row in matrix level
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
filtered = [[x for x in row if x % 3 == 0] for row in matrix if sum(row) >= 10]
print(filtered)
