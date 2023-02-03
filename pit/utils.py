#! /usr/bin/env python3 
"""Miscellaneous utilities for managing PIT output."""
import os
import sys
import argparse
import subprocess
from shutil import rmtree, copytree
import pandas as pd
import glob
from collections import defaultdict

def get_mutation_coverage(resultspath):
    """Gets mutation coverage for the project at resultspath."""
    names = ['fileName', 'className', 'mutator', 'method', 'lineNumber', \
            'status', 'killingTest']
    try:
        mutations = pd.read_csv(resultspath, names=names)
        if not mutations.empty:
            killed = ['KILLED', 'TIMED_OUT'] # pylint: disable=unused-variable
            nkilled = len(mutations.query('status in @killed'))
            nsurvived = len(mutations) - nkilled
            coverage = nkilled / len(mutations)

            result = {
                'mutants': len(mutations),
                'survived': nsurvived,
                'killed': nkilled,
                'mutationCovered': coverage
            }

            return result
    except FileNotFoundError:
        pass

    return None

def __combiner(resultspath):
    return pd.Series(get_mutation_coverage(resultspath))

def aggregate_mutation_results(dirpath, aggregate=False):
    """
    Aggregate output from mutation testing by reading PITest reports.

    Args:
        dirpath (str): Path to the directory containing tested projects
        aggregate (bool): Summarise each student's mutation score or return
                          data for all mutants?
    """
    if not os.path.isabs(dirpath):
        dirpath = os.path.abspath(dirpath)

    students = os.listdir(dirpath)
    resultpaths = {}  

    results = []

    for student in students:
        student_directory = os.path.join(dirpath, student)
        student_submissions = os.listdir(student_directory)
        for submission in student_submissions:
            submission_path = os.path.join(student_directory, submission)
            csvfiles = glob.glob(os.path.join(submission_path, '**', '*.csv'), recursive=True)
            # mutationshtml = os.path.join(projpath, 'pitReports', 'com.example')

            # Are there mutation results to speak of?
            # Each project should have a single .csv result file
            # Thus, if a project ran PIT successfully, then csvfiles should only
            # contain a singular .csv file
            if csvfiles and os.path.isfile(csvfiles[0]): 
                if aggregate:
                    results.append(pd.read_csv(csvfiles[0]))
                else:
                    resultpaths[student + "_" + submission] = csvfiles[0]
                    resultpaths
    
    if aggregate:
        return pd.concat(results)

    mutationcoverage = pd.Series(resultpaths).apply(__combiner)
    mutationcoverage.reset_index(inplace=True)
    mutationcoverage[['userName','submissionNo']] = mutationcoverage['index'].str.split('_', expand=True)
    mutationcoverage.drop('index', axis=1, inplace=True)
    mutationcoverage.set_index(['userName', 'submissionNo'], inplace=True)
    return mutationcoverage

