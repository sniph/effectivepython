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
# dict fresh_fruit
fresh_fruit = {#standard dict key/value pairs
    "apple": 10,
    "banana": 8,
    "lemon": 5,
}
print(fresh_fruit)


# Example 2
def make_lemonade(count):
    # get the value from the dict from key
    # => is int part of str:int
    # with get method
    print(f"Making {count} lemons into lemonade")


def out_of_stock():
    print("Out of stock!")


count = fresh_fruit.get("lemon", 0)#get value by key
print(count)
if count:  # if count exitst are ther lemons?
    # 0 evaluates to false
    make_lemonade(count)
else:
    out_of_stock()


# Example 3
# if count true  then count gets value by assign with ":="
if count := fresh_fruit.get("lemon", 0):#take the value for evaluation in if >0 True
    make_lemonade(count)
else:
    out_of_stock()


# Example 4
def make_cider(count):
    print(f"Making cider with {count} apples")


count = fresh_fruit.get("apple", 0)#get value according to key from dict
print(count)
if count >= 4:
    make_cider(count)
else:
    out_of_stock()


# Example 5
# short version with direct assign to count variable
if (count := fresh_fruit.get("apple", 0)) >= 4:#assign get value to var and test in compare with if 
    make_cider(count)
else:
    out_of_stock()


# Example 6
def slice_bananas(count):
    print(f"Slicing {count} bananas")
    return count * 4


class OutOfBananas(Exception):
    pass
    #out_of_stock()


def make_smoothies(count):
    print(f"Making a smoothies with {count} banana slices")


pieces = 0
count = fresh_fruit.get("banana", 0)

if count >= 2:
    pieces = slice_bananas(count)

try:
        smoothies = make_smoothies(pieces)#if pieces <2 then except
# except not triggered by count in any way why create a class? maybe to trigger except?
except OutOfBananas:
    out_of_stock()

class OutOfBananas(Exception):
    pass


#def slice_bananas(count):
 #   return count // 2


# def make_smoothies(count):
#     print(f"Making a smoothie with {count} banana slices")


count = fresh_fruit.get("banana", 0)

if count >= 2:
    pieces = slice_bananas(count)
    try:
        smoothies = make_smoothies(pieces)
    except OutOfBananas:
        #raise OutOfBananas("Not enough bananas to make smoothies")
        out_of_stock()
    
else: #the else is now calling exception
    OutOfBananas()
    out_of_stock()
    
# Example 7
# count = fresh_fruit.get("banana", 0)
class OutOfBananas(Exception):
    pass
    #out_of_stock()
count = 0  # doens't trigger the exception?
if count >= 2:
    pieces = slice_bananas(count)
else:
    #OutOfBananas()
    pieces = 0

try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()
#==============================
def out_of_stock():
    print("Out of stock!")

def slice_bananas(count):
    pass


class OutofBananas(Exception):
    pass


def make_smoothies(count):
    pass


fresh_fruit = {
    'apple': 10,
    'banana': 0,
    'lemon': 5,
}

pieces = 0
count = fresh_fruit.get('banana', 0)
if count >= 2:
    pieces = slice_bananas(count)

try:
    smoothies = make_smoothies(pieces)
except OutofBananas:
    out_of_stock()


=====================

# Example 8
pieces = 0
# direct assign values to count and test
if (count := fresh_fruit.get("banana", 0)) >= 2:
    pieces = slice_bananas(count)
    

try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()


# Example 9
# no initial values for pieces only if is true and
# else pieces = 0 (even if there is 1 banana)
if (count := fresh_fruit.get("banana", 0)) >= 2: #assign direct to count and evaluate with if
    pieces = slice_bananas(count)
else:
    pieces = 0

try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()


# Example 10
# test in steps if/else if true then stop
count = fresh_fruit.get("banana", 0)#get the valu through key
if count >= 2:
    pieces = slice_bananas(count)#print the function slice_banabas "Slicing 2 bananas" return of print for var pieces is None by default but there is a retun value in function 4*count
    to_enjoy = make_smoothies(pieces) #print the function make_smoothies return print statement is None, no later retun value to add to to_enjoy
else:
    count = fresh_fruit.get("apple", 0)
    if count >= 4:
        to_enjoy = make_cider(count)
    else:
        count = fresh_fruit.get("lemon", 0)
        if count:
            to_enjoy = make_lemonade(count)
        else:
            to_enjoy = "Nothing"
print(to_enjoy) #is None as is the return value from print statement
print(pieces) #return value count*4


# Example 11
# if true then run functions otherwise elif
if (count := fresh_fruit.get("banana", 0)) >= 2:#test and assign in one multiple if/elif or else block
    pieces = slice_bananas(count)
    to_enjoy = make_smoothies(pieces)
elif (count := fresh_fruit.get("apple", 0)) >= 4:
    to_enjoy = make_cider(count)
elif count := fresh_fruit.get("lemon", 0):
    to_enjoy = make_lemonade(count)
else:
    to_enjoy = "Nothing"


# Example 12
#several dicts in a list
FRUIT_TO_PICK = [
    {"apple": 1, "banana": 3},
    {"lemon": 2, "lime": 5},
    {"orange": 3, "melon": 2},
]
print(FRUIT_TO_PICK)

def pick_fruit():
    if FRUIT_TO_PICK:
        return FRUIT_TO_PICK.pop(0)
    else:
        return []
print(FRUIT_TO_PICK)
print(pick_fruit())


def make_juice(fruit, count):#make list of tuples from fruit/count pair
    return [(fruit, count)]

#print(make_juice(fruit ,count = fresh_fruit))

bottles = []
#every call of fresh_fruit gives a new dict {'apple': 1, 'banana': 3} etc.
#due to pop(0) over list
fresh_fruit = pick_fruit()
print(fresh_fruit)
while fresh_fruit: #as long as the list is not []
    for fruit, count in fresh_fruit.items(): #take key,value from list
        batch = make_juice(fruit, count)
        bottles.extend(batch)#appand batch to list bottles
    fresh_fruit = pick_fruit() #functional  code repeat till
    #fresh_fruit = [] by pop(0) atribute

print(bottles)
   """_summary_
for fruit, count in fresh_fruit.items(): #take key,value from list
        batch = make_juice(fruit, count)
        print('batch',batch)
        bottles.extend(batch)
        print('bottles',bottles)
fresh_fruit = pick_fruit() 
 
    """

# Example 13
FRUIT_TO_PICK = [
    {"apple": 1, "banana": 3},
    {"lemon": 2, "lime": 5},
    {"orange": 3, "melon": 2},
]
print(FRUIT_TO_PICK)

bottles = []
while True:  # Loop without end loads all to list
    fresh_fruit = pick_fruit() #first set from list by pop(0)
    if not fresh_fruit:  # And a half => if fresh_fruit = [] 
        #because not false/[] gives True then break the loop
        break
    #as long as fresh_fruit is True not empty
    for fruit, count in fresh_fruit.items():#assign key/value to fruit/count pair from list
        batch = make_juice(fruit, count)
        bottles.extend(batch)#add to bottles list

print(bottles)


# Example 14
    FRUIT_TO_PICK = [
        {"apple": 1, "banana": 3},
        {"lemon": 2, "lime": 5},
        {"orange": 3, "melon": 2},
    ]
    print(FRUIT_TO_PICK)

    bottles = []
    #as long fresh_fruit is not [] assign set with pop(0) 
    while fresh_fruit := pick_fruit():#assign to list for all items as long True
        for fruit, count in fresh_fruit.items():#loop over list assign to fruit/count pair
            batch = make_juice(fruit, count)#make list of tuples
            bottles.extend(batch)#add to bottles list
        print(fresh_fruit)

    print(bottles)
