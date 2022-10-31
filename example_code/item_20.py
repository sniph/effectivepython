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
# test try block division catch ZeroDivisionError with return None
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


assert careful_divide(4, 2) == 2
assert careful_divide(0, 1) == 0
assert careful_divide(3, 6) == 0.5
assert careful_divide(1, 0) == None


# Example 2
x, y = 1, 0
result = careful_divide(x, y)
# zero division return "None" true when message else result
if result is None:
    print("Invalid inputs")
else:
    print("Result is %.1f" % result)


# Example 3
x, y = 0, 5
result = careful_divide(x, y)
print(result)
# result of 0 evaluates to false (not false => true) if true get activated wrongly
if not result:
    print("Invalid inputs")  # This runs! But shouldn't
else:
    assert False


# Example 4
# use with test extra value true/false
def careful_divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None


assert careful_divide(4, 2) == (True, 2)
assert careful_divide(0, 1) == (True, 0)
assert careful_divide(3, 6) == (True, 0.5)
assert careful_divide(1, 0) == (False, None)

print(careful_divide(0, 1))

# test only return "None" is ZeroDivisionError
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


assert careful_divide(4, 2) == 2
assert careful_divide(0, 1) == 0
assert careful_divide(3, 6) == 0.5
assert careful_divide(1, 0) == None

print(careful_divide(0, 1))
print(careful_divide(0, 1) == 0)


# Example 5


def careful_divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None


x, y = 5, 0
# x, y = 0, 5
success, result = careful_divide(x, y)
# if success assign to false the (not false) =>True that's when y = 0 and
# returm is False,None
if not success:
    print("Invalid inputs")
print(success, result)

# Example 6
def careful_divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None


x, y = 5, 0
_, result = careful_divide(x, y)
# test on result if None the "not None" gives True for if statement
if not result:
    print("Invalid inputs")

print(not result)
print(not None)  # evaluates to True


# Example 7
# raise valueerror if ZeroDivisionError
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError("Invalid inputs")


# Example 8
x, y = 5, 0
# use the valueerror to return the message else result
try:
    result = careful_divide(x, y)
except ValueError:
    print("Invalid inputs")
else:
    print("Result is %.1f" % result)


# Example 9
a, b = 5, 0
# when ZeroDivisionError raise value error with message
def careful_divide(a: float, b: float) -> float:
    """Divides a by b.

    Raises:
        ValueError: When the inputs cannot be divided.
    """
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError("Invalid inputs")


print(careful_divide(5, 0))

# when ZeroDivisionError raise value error and is now passed
try:
    result = careful_divide(1, 0)
    assert False
except ValueError:
    pass  # Expected


assert careful_divide(1, 5) == 0.2
