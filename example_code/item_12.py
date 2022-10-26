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
x = ["red", "orange", "yellow", "green", "blue", "purple"]

odds = x[::2]  # alternating values 0,2,4
evens = x[1::2]  # alternating values 1,3,5
print(odds)
print(evens)


# Example 2
x = b"mongoose"
print(x[::1])
y = x[::-1]  # reverse values
print(y)


# Example 3
x = "寿司"
y = x[::-1]  # reverse values
print(y)


# Example 4
try:
    w = "寿司"
    x = w.encode("utf-8")
    print(x)
    y = x[::-1]
    print(y)
    z = y.decode("utf-8")
    print(z)
except:
    logging.exception("Expected")
else:
    assert False


# Example 5
x = ["a", "b", "c", "d", "e", "f", "g", "h"]
x[::2]  # ['a', 'c', 'e', 'g'] alternating step 2 starts from beginning
x[::-2]  # ['h', 'f', 'd', 'b'] alternating step -2 starts at the end of the


# Example 6
x[2::2]  # ['c', 'e', 'g'] #start pos 3 alternating step 2
x[-2::-2]  # ['g', 'e', 'c', 'a'] #start pos 2 from end alternating -2
x[-2:2:-2]  # ['g', 'e'] # pos 2 from end till pos 3 alternating -2
x[2:2:-2]  # [] # start pos 3 end pos 3 altenating -2


# Example 7
# x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
y = x[::2]  # ['a', 'c', 'e', 'g'] #start pos 0 all items alternating 2
z = y[1:-1]  # ['c', 'e'] # start pos 2 till forlast item from prev list y
print(x)
print(y)
print(z)
