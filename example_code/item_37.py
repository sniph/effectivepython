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
# no print out if no return value
# get al object lose frrom class object and test then repackage
grades = {}#create dict


def add_student(name):#add key/value pair with empty value to dict
    grades[name] = []


def report_grade(name, score):#add value to key/value pair
    grades[name].append(score)


# returns names and average_grade in tuple
def average_grade(name):#calc average over key/value
    grades2 = grades[name]
    # use grades2 instead grades name conflict
    return sum(grades2) / len(grades2)


print(grades)  # {}
add_student("Isaac Newton")#add to key/value where value is empty list in dict
print(grades)  # {'Isaac Newton': []}
# add scores to name/score dict
report_grade("Isaac Newton", 90)
report_grade("Isaac Newton", 95)
report_grade("Isaac Newton", 85)
print(grades)  # {'Isaac Newton': [90, 95, 85]} add to key/list dict


b = average_grade("Isaac Newton")#func on element of key/list dict 
print(b)  # 90.0

# then multiple functions and variable assignments packaged as class object
class SimpleGradebook:
    def __init__(self):#init dict
        self._grades = {}

    def add_student(self, name):#add key/list to dict
        self._grades[name] = []

    def report_grade(self, name, score):#add value to key/list dict
        self._grades[name].append(score)

    # returns names and average_grade in tuple 
    def average_grade(self, name):#calc on element of key/list returns tuple
        grades = self._grades[name]
        return name, sum(grades) / len(grades)


# Example 2
# initialize book variable as new class SimpleGradebook
book = SimpleGradebook()#create instance of key/list dict
book.add_student("Isaac Newton")#add element to key/list dict


book.report_grade("Isaac Newton", 90)#add value to key/list dict
book.report_grade("Isaac Newton", 95)
book.report_grade("Isaac Newton", 85)

print(book.average_grade("Isaac Newton"))#returns tuple from func


# Example 3
from collections import defaultdict


class BySubjectGradebook:
    def __init__(self):
        self._grades = {}  # Outer dict

    def add_student(self, name):
        self._grades[name] = defaultdict(list)  # Inner dict key-key/list construct

    # Example 4
    def report_grade(self, name, subject, grade):
        by_subject = self._grades[name]#key
        grade_list = by_subject[subject]#second key
        grade_list.append(grade)#add to key-key/list construct
        # return grade_list

    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total / count


# Example 5
book = BySubjectGradebook()#instanciated new class
#print((book.add_student))
book.add_student("Albert Einstein")
book.report_grade("Albert Einstein", "Math", 75)
book.report_grade("Albert Einstein", "Math", 65)
book.report_grade("Albert Einstein", "Gym", 90)
book.report_grade("Albert Einstein", "Gym", 95)


print(book.average_grade("Albert Einstein"))
print(book._grades)#{'Albert Einstein': defaultdict(<class 'list'>, {'Math': [75, 65], 'Gym': [90, 95]})} ->key-key/list construct

# class BySubjectGradebook:
# def __init__(self):
grades = {}  # Outer dict define empty dict


def add_student(name):
    grades[name] = defaultdict(list)  # Inner dict define key ->key/list structure with default dict


# Example 4
def report_grade(name, subject, grade):#construct from other functions
    by_subject = grades[name]
    grade_list = by_subject[subject]
    grade_list.append(grade)
    return name, by_subject, grade_list#return defined as tuple


def average_grade(name):#constuct data from other functions defined
    by_subject = grades[name]
    total, count = 0, 0
    for grades in by_subject.values():#loop over subjects 
        total += sum(grades)
        count += len(grades)
    return total / count

#for name setup defaultdict no value then "None" also set per "subject:[list of grades]"
# book = BySubjectGradebook()
add_student("Albert Einstein")
print(grades)
report_grade("Albert Einstein", "Math", 75)
# print(report_grade("Albert Einstein", "Math", 75))

report_grade("Albert Einstein", "Math", 65)
report_grade("Albert Einstein", "Gym", 90)
report_grade("Albert Einstein", "Gym", 95)#('Albert Einstein', defaultdict(<class 'list'>, {'Math': [75, 65], 'Gym': [90, 95]}), [90, 95])


print(average_grade("Albert Einstein"))


# Example 6
class WeightedGradebook:#incorparated functions in 1 class
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = defaultdict(list)

    def report_grade(self, name, subject, score, weight):
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append((score, weight))

    # Example 7
    def average_grade(self, name):
        by_subject = self._grades[name]

        score_sum, score_count = 0, 0
        for subject, scores in by_subject.items():
            subject_avg, total_weight = 0, 0
            for score, weight in scores:
                subject_avg += score * weight
                total_weight += weight

            score_sum += subject_avg / total_weight
            score_count += 1

        return score_sum / score_count


# Example 8
book = WeightedGradebook()#uses class with extra var weight
book.add_student("Albert Einstein")
book.report_grade("Albert Einstein", "Math", 75, 0.05)
book.report_grade("Albert Einstein", "Math", 65, 0.15)
book.report_grade("Albert Einstein", "Math", 70, 0.80)
book.report_grade("Albert Einstein", "Gym", 100, 0.40)
book.report_grade("Albert Einstein", "Gym", 85, 0.60)
print(book.average_grade("Albert Einstein"))


# Example 9
grades = []#define var as list
grades.append((95, 0.45))
grades.append((85, 0.55))
total = sum(score * weight for score, weight in grades)#expression and loop in sum function
total_weight = sum(weight for _, weight in grades)#direct way to use function on data iterable by sum
average_grade = total / total_weight
print(average_grade)


# Example 10
grades = []#easy expand list of tuples with extra var
grades.append((95, 0.45, "Great job"))
grades.append((85, 0.55, "Better next time"))
print(grades)#[(95, 0.45, 'Great job'), (85, 0.55, 'Better next time')]
total = sum(score * weight for score, weight, _ in grades)
total_weight = sum(weight for _, weight, _ in grades)
average_grade = total / total_weight
print(average_grade)


# Example 11
from collections import namedtuple

Grade = namedtuple("Grade", ("score", "weight"))#define structure of grade


# Example 12
class Subject:
    def __init__(self):
        self._grades = []#define list

    def report_grade(self, score, weight):#add tuple to list
        self._grades.append(Grade(score, weight))

    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


# Example 13
class Student:
    def __init__(self):#create object of dict type with default dict with interaction to othre class methods
        self._subjects = defaultdict(Subject)

    def get_subject(self, name):
        return self._subjects[name]

    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count


# Example 14
class Gradebook:#set an object as dict in overall class
    def __init__(self):
        self._students = defaultdict(Student)

    def get_student(self, name):
        return self._students[name]


# Example 15
book = Gradebook()#instanciated overall class with links to other class/methods
albert = book.get_student("Albert Einstein")
math = albert.get_subject("Math")
math.report_grade(75, 0.05)
math.report_grade(65, 0.15)
math.report_grade(70, 0.80)
gym = albert.get_subject("Gym")
gym.report_grade(100, 0.40)
gym.report_grade(85, 0.60)
print(albert.average_grade())
