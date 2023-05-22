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
# create generator "it" call with next method yield values till .throw exception raised
try:

    class MyError(Exception):
        pass

    def my_generator():#yield make func generator object
        yield 1
        yield 2
        yield 3

    it = my_generator()#instance of generator
    print(next(it))  # Yield 1 call generator once
    print(next(it))  # Yield 2 call generator twice
    print(it.throw(MyError("test error")))#way to get error by throw method
except:
    logging.exception("Expected")
else:
    assert False


# Example 2
# first call with next value 1, second call with next value 2 in try block
# third call with next value after yield output value 4 throw error(receive and send part in call for throws exception)
def my_generator():
    yield 1#first call

    try:
        yield 2#second call
    except MyError:#thirt is an except because try loop has one value then execpt
        print("Got MyError!")
    else:
        yield 3

    yield 4


it = my_generator()#value 1 ,2 can be reached 3 ,4 not with next method on generator
print(next(it))  # Yield 1
print(next(it))  # Yield 2
print(it.throw(MyError("test error")))


# Example 3
class Reset(Exception):
    pass


# "timer" generator function counts back to zero
def timer(period):
    current = period#assign var with value
    while current:#
        current -= 1
        try:
            yield current #after last yield except ->class pass
        except Reset:
            current = period


print(list(timer(3)))#list calls all yields of generator to list [2, 1, 0]

# Example 4
class Reset(Exception):
    pass


RESETS = [
    False,  # value 3 => 0,1,2,3 timer(4)
    False,  # value 2 => 0,1,2,3
    False,  # value 1 => 0,1,2,3
    True,  # reset to original state value timer 4
    False,
    True,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
]

# if True ok else will deliver False trigger exception pop values from left to right in Reset list
def check_for_reset():
    # Poll for external event
    return RESETS.pop(0)


# after every item in Reset list announce remaining values timer cycles
def announce(remaining):
    print(f"{remaining} ticks remaining")


def run():
    it = timer(4)  # 0,1,2,3 =>4 times
    # while runs loop till exception is raised triggered by RESETS list
    while True:
        try:
            # throw error if RESETS list has True value
            if check_for_reset():
                current = it.throw(
                    Reset()
                )  # call class method as pass and except in timer reset current = period original position

            else:
                current = next(it)
        # if no timer cycles StopIteration exception is raised and break out of loop
        except StopIteration:
            break
        # after every cycle else part of try block returns announce print remaining cycles
        else:
            announce(current)#will be called every loop ->"3 ticks remaining" etc.


run()


# Example 5
class Timer:#compact class with vars init, reset and iter method we'll use for this exemple
    def __init__(self, period):
        self.current = period
        self.period = period

    def reset(self):
        self.current = self.period

    def __iter__(self):#creates generator
        while self.current:
            self.current -= 1
            yield self.current


# Example 6
RESETS = [
    False,
    False,
    True,
    False,
    True,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
]


def run():
    # initialize Timer class =>"timer " variable with 4 cycles
    timer = Timer(4)#timer class gives a generator
    # loop over timer check RESETS list if True rest, announce per cycle interval
    # every event as function in class makes it more obvious
    for current in timer:#loop over generator
        if check_for_reset():  # check RESETS list very clear false/true in list
            timer.reset()  # reset timer reset period
        announce(current)


run()
