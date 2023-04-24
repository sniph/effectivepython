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
from random import randint

random_bits = 0
for i in range(32):
    if randint(0, 1):
        # 1<< 1 means 0010 following zeros
        # 1101 | 0010 => 1111 add bits
        # xxxx | 0010 = xx1x (All the other bits remain the same)
        random_bits |= 1 << i

print(bin(random_bits))


# Example 2
flavor_list = ["vanilla", "chocolate", "pecan", "strawberry"]
for flavor in flavor_list: #iterate over list print ,with F" format
    # iterate over list
    print(f"{flavor} is delicious")


# Example 3
for i in range(len(flavor_list)):#check lengt list,iterate with i over list
    # i is 0,1,2
    flavor = flavor_list[i]
    # index 0 + 1 etc.
    print(f"{i + 1}: {flavor}")


# Example 4
it = enumerate(flavor_list)#iterate stepwise by next method
# iterate first (0, 'vanilla')
print(next(it))
# iterate second (1, 'chocolate')
print(next(it))


# Example 5
for i, flavor in enumerate(flavor_list):#iterate with enumerate no length, auto i indexing
    # i is 0,1,2
    # index 0+1 etc.
    print(f"{i + 1}: {flavor}")


# Example 6
for i, flavor in enumerate(flavor_list, 1): #iterate with enumerate and index start is 1
    # i is 0,1,2
    # index starting from 1 in enumerate
    print(f"{i}: {flavor}")
