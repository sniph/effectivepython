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
# function with try block for overflow and ZeroDivisionError
def safe_division(number, divisor, ignore_overflow, ignore_zero_division):
    try:
        return number / divisor
    except OverflowError:#proceeds because of intercept error else raise and true/false flag of kind of error
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float("inf")
        else:
            raise


# Example 2
# assign 4 values for call of function
result = safe_division(1.0, 10**500, True, True)
print(result)


# Example 3
# set exepct false/true if needed
result = safe_division(1.0, 0, False, True)#intercept error by except and true/false flag of kind of error else raise error
print(result)


# Example 4
# default keyword arguments set to false in executio set to True
def safe_division_b(
    number, divisor, ignore_overflow=False, ignore_zero_division=False  # Changed
):  # Changed
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float("inf")
        else:
            raise


# Example 5
# sets 1 keyword argument to True other is still default
result = safe_division_b(1.0, 10**500, ignore_overflow=True)
print(result)

result = safe_division_b(1.0, 0, ignore_overflow=True)#error division as default error
print(result)

# sets 1 keyword argument to True other is still default
result = safe_division_b(1.0, 0, ignore_zero_division=True)
print(result)

result = safe_division_b(1.0, 10**500, ignore_zero_division=True)#not except for overflow is default error
print(result)


# Example 6
# even positinal ovverride of defaults in function
assert safe_division_b(1.0, 10**500, True, False) == 0#overflow except is set to true positional
print(safe_division_b(1.0, 10**500, True, False))

# Example 7
# use of "*" after arguments, raises error if keyword arguments are given as postional
def safe_division_c(
    number, divisor, *, ignore_overflow=False, ignore_zero_division=False  # unclear number pos args by *
    #number, divisor,ignore_overflow=False, ignore_zero_division=False #works as tried 4 args
):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float("inf")
        else:
            raise


# Example 8
# this raise error 4 postional argument given only 2 arguments in function
# "*" and 2 keyword arguments
try:
    safe_division_c(1.0, 10**500, True, False)#4 positional args is problem
except:
    logging.exception("Expected")
else:
    assert False


# Example 9
# use 2 positional arguments and a keyword argument with assigned value
result = safe_division_c(1.0, 0, ignore_zero_division=True)#2 pos args and 1 kwarg is fine

assert result == float("inf")


try:
    result = safe_division_c(1.0, 0)#2 positional rest default
    

except ZeroDivisionError:
    print("expected:", result)

    # pass  # Expected
else:
    assert False
print(ignore_zero_division)
print(result)


# Example 10
# make use of changed arguments named or positional keyword arguments are defaulted
assert safe_division_c(number=2, divisor=5) == 0.4
assert safe_division_c(divisor=5, number=2) == 0.4
assert safe_division_c(2, divisor=5) == 0.4#because firts is positional
#assert safe_division_c(number=2, 5) == 0.4 #positional always before keywoord arg

# Example 11
# problem with argument naming call differnt from function call naming
def safe_division_c(
    numerator,
    denominator,
    *,  # Changed
    ignore_overflow=False,
    ignore_zero_division=False,
):
    try:
        return numerator / denominator
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float("inf")
        else:
            raise


# Example 12
# call with different arguments than the default
try:
    safe_division_c(number=2, divisor=5)#refer to right keyarg names
except:
    logging.exception("Expected")
else:
    assert False

try:
    safe_division_c(numerator=2, denominator=5)##refer to right keyarg names
except:
    logging.exception("Expected")
else:
    assert True

# Example 13
# "/" follows positional arguments only
def safe_division_d(
    numerator,
    denominator,
   /, #places before this token must be positional
    *,  # Changed
    ignore_overflow=False,
    ignore_zero_division=False,
):
    try:
        return numerator / denominator
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float("inf")
        else:
            raise


# Example 14
# call function with positional arguments works
assert safe_division_d(2, 5) == 0.4
print(safe_division_d(2, 5))


# Example 15
# call with keyword arguments gives error
try:
    safe_division_d(numerator=2, denominator=5)#with use of ""/" as arg befor token must positional
    #TypeError: safe_division_d() got some positional-only arguments passed as keyword arguments: 'numerator, denominator'

except:
    logging.exception("Expected")
else:
    assert False


# Example 16
def safe_division_e(
    numerator,
    denominator,
    /,  # follows positional arguments only after * keyword only
    # in between positional or keyword arguments
    ndigits=10,  # use argumet name with default value
    *,  # Changed start of keyword arguments
    ignore_overflow=False,
    ignore_zero_division=False,
):
    try:
        fraction = numerator / denominator  # Changed
        return round(fraction, ndigits)  # Changed
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float("inf")
        else:
            raise


# Example 17
# only 2 positional mandatory arguments
result = safe_division_e(22, 7)
print(result)

# third positional argument optional has default
result = safe_division_e(22, 7, 5)#3 arg between "/" and "*" can be positional are keyword arg 
print(result)

# third positional argument optional has default also named assigned
result = safe_division_e(22, 7, ndigits=2)#3 arg between "/" and "*" can be positional are keyword arg 
print(result)

# keyword argument optional has defaults can be changed too
result = safe_division_e(22, 7, ndigits=2, ignore_overflow=True)# after "*" token is keyword arg
print(result)

result = safe_division_e(22, 7, ndigits=2, True)# after "*" token is keyword arg
                                                #SyntaxError: positional argument follows keyword argument
print(result)