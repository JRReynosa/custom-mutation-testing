#! /usr/bin/env python3

"""Utility to aggregate PITest mutation data for several projects
into a CSV file for analysis.
"""

import pandas as pd
from os import listdir, path
import argparse

def __get_mutation_coverage(resultspath):
    names = [ 'fileName', 'className', 'mutator', 'method', 'lineNumber', \
            'status', 'killingTest' ]
    mutations = pd.read_csv(resultspath, names=names)
    if len(mutations) > 0:
        nkilled = len(mutations[mutations['status'] == 'KILLED'])
        nsurvived = len(mutations) - nkilled
        coverage = nkilled / len(mutations)


        return pd.Series({
            'mutants': len(mutations),
            'survived': nsurvived,
            'killed': nkilled,
            'mutationCovered': coverage
        })
    else:
        return None 

def aggregate_mutation_results(infile):
    """
    Aggregate output from mutation testing by reading PITest reports.

    Args:
        infile (str): Path to the directory containing tested projects
    """
    if (not path.isabs(infile)):
        infile = path.abspath(infile)
    
    projects = listdir(infile)
    resultpaths = {}

    for proj in projects:
        projpath = path.join(infile, proj)
        mutationscsv = path.join(projpath, 'pitReports', 'mutations.csv')
        mutationshtml = path.join(projpath, 'pitReports', 'com.example')
        
        # are there mutation results to speak of?
        if path.isfile(mutationscsv) and path.isdir(mutationshtml):
            resultpaths[proj] = mutationscsv

    mutationcoverage = pd.Series(resultpaths).apply(__get_mutation_coverage)
    mutationcoverage.index.name = 'userName'
    return mutationcoverage

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Path to PIT testing output')
    parser.add_argument('output', help='Path to output CSV file')
    args = parser.parse_args()
    
    infile = args.input
    outfile = args.output

    results = aggregate_mutation_results(infile)
    results.to_csv(path_or_buf=outfile, index=True)
