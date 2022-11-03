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
# mod number with divisor =>remainder 20-2*7=14 rest 6
def remainder(number, divisor):
    return number % divisor


assert remainder(20, 7) == 6


# Example 2
# both positional
remainder(20, 7)
# 1 positional still whole as positional
remainder(20, divisor=7)
# doesn't work need to be keyword argument
# remainder(divisor=7, 20)

# both keyword arguments can be switchted
remainder(number=20, divisor=7)
remainder(divisor=7, number=20)


# Example 3
# test change positional with keyword argument get een except message
try:
    # This will not compile
    source = """remainder(number=20, 7)"""
    eval(source)
except:
    logging.exception("Expected")
else:
    assert False


# Example 4
# test change positional with keyword argument get een except message
try:
    remainder(20, number=7)
except:
    logging.exception("Expected")
else:
    assert False


# Example 5
# read the set wiith keywords in the function with "**kwargs" not positional
my_kwargs = {
    "number": 20,
    "divisor": 7,
}
assert remainder(**my_kwargs) == 6


# Example 6
# with keyword arguments you can switch even combo with positional arguments
my_kwargs = {
    "divisor": 7,
}
assert remainder(number=20, **my_kwargs) == 6
assert remainder(20, **my_kwargs) == 6
assert (
    remainder(
        **my_kwargs,
        number=20,
    )
    == 6
)

# Example 7
# even keyword arguments from different sets work
my_kwargs = {
    "number": 20,
}
other_kwargs = {
    "divisor": 7,
}
assert remainder(**my_kwargs, **other_kwargs) == 6
# even nog the working of the function stays correct mod numbers by divisior
assert remainder(**other_kwargs, **my_kwargs) == 6
print(remainder(**other_kwargs, **my_kwargs))

# Example 8
# for every key,value pair in input function runs
def print_parameters(**kwargs):
    for key, value in kwargs.items():
        # is a list of tuples with key,value pairs
        print(kwargs.items())
        print(f"{key} = {value}")
        a = [x for x in kwargs]
        print(a)

        # print(**kwargs)


print_parameters(alpha=1.5, beta=9, gamma=4)


# Example 9
# return value of function is assigned to flow variable
def flow_rate(weight_diff, time_diff):
    return weight_diff / time_diff


weight_diff = 0.5
time_diff = 3
flow = flow_rate(weight_diff, time_diff)
# 3 cijfers achter de komma
print(f"{flow:.3} kg per second")


# Example 10
# assign return function to variable with a positional and keyword argument
def flow_rate(weight_diff, time_diff, period):
    return (weight_diff / time_diff) * period


# Example 11
# assign return function to variable with a positional and keyword argument
flow_per_second = flow_rate(weight_diff, time_diff, 1)
flow_per_second = flow_rate(time_diff, weight_diff, 1)
print(flow_per_second)


# Example 12
def flow_rate(weight_diff, time_diff, period=1):
    return (weight_diff / time_diff) * period


# Example 13
# if variable is set in runtime it's positional
flow_per_second = flow_rate(weight_diff, time_diff)
flow_per_hour = flow_rate(weight_diff, time_diff, period=3600)
# gives positional error
# flow_per_hour = flow_rate(weight_diff, period=3600, time_diff)
print(flow_per_second)
print(flow_per_hour)


# Example 14
def flow_rate(weight_diff, time_diff, period=1, units_per_kg=1):
    return ((weight_diff * units_per_kg) / time_diff) * period


# Example 15
# if you assign value in function call it overrides the default value
#
pounds_per_hour = flow_rate(weight_diff, time_diff, period=3600, units_per_kg=2.2)
print(pounds_per_hour)


# Example 16
# even if you call function with values
#default in function can also be positional again by assign values directly
pounds_per_hour = flow_rate(weight_diff, time_diff, 3600, 2.2)
print(pounds_per_hour)

#omit defaults keywords is no problem
pounds_per_hour = flow_rate(weight_diff, time_diff)
print(pounds_per_hour)

#changing position of keywords in call is no Problem
pounds_per_hour = flow_rate(time_diff, weight_diff )
print(pounds_per_hour)

#keyword with default value is optional but also positional
weight_diff = 0.5
time_diff = 3
period = 1

def flow_rate(weight_diff, time_diff, period=1, units_per_kg=1):
    return ((weight_diff * units_per_kg) / time_diff) * period

#pounds_per_hour = flow_rate(time_diff, weight_diff,period=1 )
#print(pounds_per_hour)
period=2
#assign new value to keyword arg makes it positional
pounds_per_hour = flow_rate(period=2, time_diff, weight_diff )
print(pounds_per_hour)


