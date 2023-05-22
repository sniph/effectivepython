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
def get_stats(numbers):#function input number output tuple (min,max)
    minimum = min(numbers)
    maximum = max(numbers)
    return minimum, maximum


lengths = [63, 73, 72, 60, 67, 66, 71, 61, 72, 70]

# assign/unpack the return values max.min from function
# to variables
minimum, maximum = get_stats(lengths)  # Two return values assign to vars

print(f"Min: {minimum}, Max: {maximum}")


# Example 2
# assign to values to two variables
first, second = 1, 2#assign 2 numbers to vars
assert first == 1
assert second == 2


def my_function():#function return to static numbers
    return 1, 2


# assign two values to 2 variables through function
first, second = my_function()#assign return function to vars
assert first == 1
assert second == 2


# Example 3
# lengths = [63, 73, 72, 60, 67, 66, 71, 61, 72, 70]
# function accept list return list by list comprehension
def get_avg_ratio(numbers):
    average = sum(numbers) / len(numbers)
    # x divided by average to determine ratio
    scaled = [x / average for x in numbers]#every number from list divide by average
    # sort smal to big
    scaled.sort(reverse=True)#list sort reverse and assign
    return scaled


# divide/unpack list in 3 pieces 2 var and middle list
longest, *middle, shortest = get_avg_ratio(lengths)#assign parts of list to vars

print(f"Longest:  {longest:>4.0%}")
print(f"Shortest: {shortest:>4.0%}")


# Example 4
def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    count = len(numbers)
    average = sum(numbers) / count

    sorted_numbers = sorted(numbers)
    # floor division by 2  3.5 => 3 etc.
    middle = count // 2
    # define middle in even len list
    # mod count divided by 2 true then middle
    if count % 2 == 0:
        # len is 8 lower pos 4 => 0,1,2,3
        lower = sorted_numbers[middle - 1]
        # len is 8/2 = 4 pos 5 => 0,1,2,3,4
        upper = sorted_numbers[middle]
        median = (lower + upper) / 2
    else:
        # middle is oneven say 7//2 = 3(floor 3.5) pos 4 0,1,2,3
        median = sorted_numbers[middle]

    return minimum, maximum, average, median, count


# assign 5 variables from function is positional
minimum, maximum, average, median, count = get_stats(lengths)#assign return to vars

print(f"Min: {minimum}, Max: {maximum}")
print(f"Average: {average}, Median: {median}, Count {count}")

assert minimum == 60
assert maximum == 73
assert average == 67.5
assert median == 68.5
assert count == 10

# Verify odd count median
# variables are positional dummyvariables by "_"
# _, _, _, median, count = get_stats([1, 2, 3])
_, _, _, median, count = get_stats([1, 2, 3])#assign only two of 5 vars
assert median == 2
assert count == 3


# Example 5
# Correct:
# positional names function local scop
minimum, maximum, average, median, count = get_stats(lengths)
print(f"Min: {minimum}, Max: {maximum}")
print(f"Average: {average}, Median: {median}, Count {count}")

# Oops! Median and average swapped:
minimum, maximum, median, average, count = get_stats(lengths)#assign is positional
print(f"Min: {minimum}, Max: {maximum}")
print(f"Average: {average}, Median: {median}, Count {count}")


# Example 6
# advise never unpack more than 3 items
minimum, maximum, average, median, count = get_stats(lengths)

minimum, maximum, average, median, count = get_stats(lengths)

(minimum, maximum, average, median, count) = get_stats(lengths)

(minimum, maximum, average, median, count) = get_stats(lengths)
