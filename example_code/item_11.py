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
a = ["a", "b", "c", "d", "e", "f", "g", "h"]
print("Middle two:  ", a[3:5])
print("All but ends:", a[1:7])


# Example 2
# list tot 5 =>0,1,2,3,4
assert a[:5] == a[0:5]
print(a[:5], "==", a[0:5])


# Example 3
# from item 6,7,8 pos 6 is included
assert a[5:] == a[5 : len(a)]
print(a[5:], " ==", a[5 : len(a)])


# Example 4
# a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print(a[:])  # all items
print(a[:5])  # till pos 6 a-e
print(a[:-1])  # a-g last item not included
print(a[4:])  # e-h 5e pos included
print(a[-3:])  # f-h 3e from end incl
print(a[2:5])  # pos 3 till 6 =>c-e (f not included)
print(a[2:-1])  # 3e pos till 1e from end (c-g)
print(a[-3:-1])  # 3e pos from end till 1e from end (f-g)


# Example 5
# see exemp 4
a[:]  # ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
a[:5]  # ['a', 'b', 'c', 'd', 'e']
a[:-1]  # ['a', 'b', 'c', 'd', 'e', 'f', 'g']
a[4:]  #                     ['e', 'f', 'g', 'h']
a[-3:]  #                          ['f', 'g', 'h']
a[2:5]  #           ['c', 'd', 'e']
a[2:-1]  #           ['c', 'd', 'e', 'f', 'g']
a[-3:-1]  #                          ['f', 'g']


# Example 6
# means all list shorter then 20 items
first_twenty_items = a[:20]
print(first_twenty_items)

# means all list shorter then 20 items
last_twenty_items = a[-20:]
print(last_twenty_items)

# Example 7
# item 20 doesn't exist in the list
try:
    a[20]
except:
    logging.exception("Expected")
else:
    assert False


# Example 8
# a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
b = a[3:]
print("Before:   ", b)  # d-h
b[1] = 99
print("After:    ", b)  # 2 pos is 99
print("No change:", a)  # all


# Example 9
# replace part of list with new list
print("Before ", a)
a[2:7] = [99, 22, 14]  # 3 pos till pos 8 => c-g = 99,22,14
print("After  ", a)


# Example 10
# Before  ['a', 'b', 99, 22, 14, 'h']
print("Before ", a)
a[2:3] = [47, 11]  # pos 3 => 47,11
# 99 is now 47,11
print("After  ", a)


# Example 11
# a[:] assign a copy to b values are the same but a and are not identical.
# not same reference to objects with a = b values and ref is the same
b = a[:]  # b gets copy of a values are the same reference not
print(b)
print(a)
assert b == a and b is not a  # True(same values) and True(not same ref/object)
print(b == a, "and", b is not a)
print(id(a) == id(b))

# Example 12
b = a
print(id(a) == id(b))
print("Before a", a)
print("Before b", b)
assert b == a and b is not a
print(b == a, "and", b is not a)
print(id(a) == id(b))

a[:] = [101, 102, 103]
print(b)
print(a)
print(id(a) == id(b))
assert a is b  # Still the same list object
print("After a ", a)  # Now has different contents
print("After b ", b)  # Same list, so same contents as a
assert b == a and b is not a
assert b is not a
print(b == a, "and", b is not a)
print(id(a) == id(b))
