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
# seems to return the same datetime at separate
# calls of function
from time import sleep
from datetime import datetime


def log(message, when=datetime.now()):
    print(f"{when}: {message}")


log("Hi there!")#current time
sleep(0.1)#delay of 0.1 sec
log("Hello again!")#still old urrent time no refresh


# Example 2
# by assigning  "None" as default keyword argument
# test on "None" then assign datetime again gives
# different results
def log(message, when=None):
    """Log a message with a timestamp.

    Args:
        message: Message to print.
        when: datetime of when the message occurred.
            Defaults to the present time.
    """
    if when is None:#always True
        when = datetime.now()#assign current time every call to var when
    print(f"{when}: {message}")


# Example 3
# run the function twice assign datetime twice
log("Hi there!")#current time
sleep(0.1)
log("Hello again!")#refreshed current time new call new assign to var


# Example 4
import json

# default variables doesn't have to be called only data
# one set created and used in both calls
def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default


# Example 5
# 2 calls of function same set returns with added value data
foo = decode("bad data")#this assign {} to "bad data:"
print("bad data:", foo)

foo["stuff"] = 5
print("Foo:", foo)
print("bad data:", foo)#also item added to dict
print(foo)

bar = decode("also bad")
print("Foo:", foo)
print("Bar:", bar)
print(foo)


bar["meep"] = 1
print("Foo:", foo)#bar and foo reference to foo dict "{'stuff': 5, 'meep': 1}"
print("Bar:", bar)
print(foo)

# Example 6
# 2 calls same return for separate variables
assert foo is bar#bar and foo reference to foo dict "{'stuff': 5, 'meep': 1}"
print(foo is bar)


# Example 7
# assign "None" as default and return result try block with test
# every call to function gives a new set
def decode(data, default=None):#by default = None instead {} cuases reload of json to seperate dicts
    """Load JSON data from a string.

    Args:
        data: JSON data to decode.
        default: Value to return if decoding fails.
            Defaults to an empty dictionary.
    """
    try:
        return json.loads(data)
    except ValueError:
        if default is None:
            default = {}#create new dict per name
        return default


# Example 8
# 2 variables with the data from seperate calls
foo = decode("bad data")
foo["stuff"] = 5
print(foo)#seperate assign to dict
bar = decode("also bad")
bar["meep"] = 1
print(bar)

print("Foo:", foo)
print("Bar:", bar)
assert foo is not bar#seperate assign to dict
