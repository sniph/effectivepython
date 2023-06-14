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
class Homework:#getter snd setter with property decorator
    def __init__(self):
        self._grade = 0#init var

    @property
    def grade(self):
        print('grade.getter',self._grade)
        return self._grade#see init var

    @grade.setter
    def grade(self, value):
        print('grade.setter', value)
        if not (0 <= value <= 100):
            raise ValueError(
                'Grade must be between 0 and 100')
        self._grade = value


# Example 2
galileo = Homework()
galileo.grade = 95#grade.setter 95
assert galileo.grade == 95#grade.getter 95


# Example 3
class Exam:#double getter and setter with decorator property and internal method with decorator staticmethod
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0#init vars

    @staticmethod#method within class to operate generic on vars
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError(
                'Grade must be between 0 and 100')


# Example 4
    @property
    def writing_grade(self):
        print('grade.getter_writing',self._writing_grade)
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, value):
        print('grade.setter_check_writing',self._check_grade(value))
        print('grade.setter_writing',self._writing_grade)
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        print('grade.getter_math',self._math_grade)
        return self._math_grade

    @math_grade.setter
    def math_grade(self, value):
        print('grade.setter_check_math',self._check_grade(value))
        print('grade.setter_math',self._math_grade)
        self._check_grade(value)
        self._math_grade = value

galileo = Exam()
galileo.writing_grade = 85
galileo.math_grade = 99
galileo.math_grade = 101#ValueError: Grade must be between 0 and 100

assert galileo.writing_grade == 85
assert galileo.math_grade == 99


# Example 5
class Grade:
    def __get__(self, instance, instance_type):
        pass

    def __set__(self, instance, value):
        pass

class Exam:
    # Class attributes
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


# Example 6
exam = Exam()
exam.writing_grade = 40
print(exam.writing_grade)


# Example 7
Exam.__dict__['writing_grade'].__set__(exam, 40)


# Example 8
exam.writing_grade
print(list(exam.writing_grade))

# Example 9
Exam.__dict__['writing_grade'].__get__(exam, Exam)
a=Exam.__dict__['writing_grade'].__get__(exam, Exam)
print(a)

print(exam.writing_grade)
print(Exam.__dict__['writing_grade'].__get__(exam, Exam))

# Example 10
class Grade:#get set and int method with dunder notation in class
    def __init__(self):
        self._value = 0

    def __get__(self, instance, instance_type):#return value
        return self._value

    def __set__(self, instance, value):#set and check on value
        if not (0 <= value <= 100):
            raise ValueError(
                'Grade must be between 0 and 100')
        self._value = value


# Example 11
class Exam:#init vars from generic class
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

first_exam = Exam()#init var with methods to call on generic class
first_exam.writing_grade = 82
first_exam.science_grade = 99
print('Writing', first_exam.writing_grade)
print('Science', first_exam.science_grade)


# Example 12
second_exam = Exam()#overwrite of first init of class
second_exam.writing_grade = 75
print(f'Second {second_exam.writing_grade} is right')
print(f'First  {first_exam.writing_grade} is wrong; '
      f'should be 82')


# Example 13
class Grade:#generic set and get with init all as dunder methods 
    def __init__(self):
        self._values = {}#int var as dict

    def __get__(self, instance, instance_type):#return dict
        print(instance,instance_type)
        if instance is None:
            return self
        print('getter_key_value',self._values.get(instance))
        print('getter_key_values',self._values)#getter_key_value {<__main__.Exam object at 0x0000019757FAEE90>: 82, <__main__.Exam object at 0x0000019757FAC490>: 75}
                                    #returns dict of all key/values
        return self._values.get(instance, 0)#returns value for this key/value from dict as is currently set

    def __set__(self, instance, value):#set value for dict
        if not (0 <= value <= 100):
            raise ValueError(
                'Grade must be between 0 and 100')
        #print('setter_key_value',self._values[instance])
        self._values[instance] = value


        
class Exam:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

first_exam = Exam()#first instance value in dict

first_exam.writing_grade = 82
second_exam = Exam()#second value in dict
second_exam.writing_grade = 75
print(f'First  {first_exam.writing_grade} is right')
print(f'Second {second_exam.writing_grade} is right')



# Example 14
from weakref import WeakKeyDictionary

class Grade:
    def __init__(self):#init dictonary for temperary keys only to get seperate instances looks like the set {} init method but cleaner
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError(
                'Grade must be between 0 and 100')
        self._values[instance] = value


# Example 15
class Exam:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 82
second_exam = Exam()
second_exam.writing_grade = 75
print(f'First  {first_exam.writing_grade} is right')
print(f'Second {second_exam.writing_grade} is right')
