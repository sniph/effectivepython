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
# yield returns an item per call
def move(period, speed):#generator object use next or list to unpack
    for _ in range(period):
        yield speed


def pause(delay):#generator object use next or list to unpack
    for _ in range(delay):
        yield 0


# Example 2
# yield the different functions
def animate():#generator object use next or list to unpack
    for delta in move(4, 5.0):
        yield delta
    for delta in pause(3):
        yield delta
    for delta in move(2, 3.0):
        yield delta


# will execute 4 times with next over animate function
print(next(animate()))#get next item
# call "animate" function with "list" method assign to "a" list
a = list(animate())#get all remaining items after next method
print(a)

# Example 3
def render(delta):
    print(f"Delta: {delta:.1f}")
    # Move the images onscreen


# run as a decorator for animate function
def run(func):
    for delta in func():
        render(delta)


run(animate)#animate func as input to func run and then func render as way to decoration


# Example 4
# "yield from" statement is same as "yield" but place in function differnt
# yield makes a generator function
def animate_composed():#use yield without loop statement same effect
    yield from move(4, 5.0)
    yield from pause(3)
    yield from move(2, 3.0)


# "run" function as decorator for animate_composed to process deltas
run(animate_composed)


# Example 5
import timeit


def child():
    for i in range(1_000_000):
        yield i


# loop over loop with yield
def slow():#here it's yield over yield twice same method
    for i in child():
        yield i


# get one loop over yield more direct
def fast():#here "yield from" method over yield is faster runtime and shorter code
    yield from child()


# test yield methods yield in for loop against "yield from" direct function
baseline = timeit.timeit(stmt="for _ in slow(): pass", globals=globals(), number=50)
print(f"Manual nesting {baseline:.2f}s")

comparison = timeit.timeit(stmt="for _ in fast(): pass", globals=globals(), number=50)
print(f"Composed nesting {comparison:.2f}s")

reduction = -(comparison - baseline) / baseline
print(f"{reduction:.1%} less time")
