import sys
import os
import utils
import pandas as pd

# SP23 Virginia Tech Undergraduate Research under Rifat Sabbir Mansur
# Jonathan Reynosa (jonathanreynosa)

# The following two functions are from the utils.py file (imported above) 
# from the GitHub repository 'sensordata' created by GitHub User and 
# Researcher 'ayaankazerouni'

# Function #1:
# raw_to_csv(inpath: str, outpath: str, fieldnames=None) -> None:

# Function #2:
# maptouuids(sensordata=None, sdpath=None, uuids=None, uuidpath=None, crnfilter=None,
#               crncol='crn', usercol='email', assignmentcol='CASSIGNMENTNAME', due_dates=None):

# Script created to run function #1 on raw DevEvent data files. The raw 
# DevEvent data files should be comprised of newline seperated URLs. The
# output of function #1 is a CSV file for each DevEvent data file. The CSVs
# output from function #1 and a user provided UUID file is then provided to
# functions #2 to map the sensor and UUID data, and the results of this are
# outputted as a final CSV file titled mapping_output.csv.
# _______________________________________________________________________________________ #

# Usage
if not len(sys.argv) == 5:
        print('Usage:\n\t./csv_and_uuid_mapping.py', end =" ")
        print('<Input Dir> <CSV Output Dir> <UUID CSV File> <Merged Output Dir>')
        print('\n\tInput Dir - Directory containing raw sensor data files composed of newline seperated URLs')
        print('\n\tCSV Output Dir - Directory to which the results of raw_to_csv() will be directed')
        print('\n\tUUID CSV File - CSV file containing student and project UUIDs')
        print('\n\tMapping Output Dir - Directory to which the results of maptouuids() will be directed')
        sys.exit()

# Read arguments
input_dir = sys.argv[1]
csv_out_dir = sys.argv[2]
uuid_file = sys.argv[3]
map_out_dir = sys.argv[4]

# Field names specific to the raw sensor data, which is a file of newline separated URLs
fieldnames = [
    'studentProjectUuid',
    'userUuid',
    'time',
    'runtime',
    'tool',
    'sensorDataType',
    'uri'
]

# Make directories if they don't already exist
if not os.path.exists(csv_out_dir):
    os.makedirs(csv_out_dir)
if not os.path.exists(map_out_dir):
    os.makedirs(map_out_dir)

# Iterate raw sensor data files in input directory and use raw_to_csv() to get a CSV
# file output for each sensor data file
for filename in os.listdir(input_dir):
    f = os.path.join(input_dir, filename)
    if os.path.isfile(f):
        output_file_name = csv_out_dir + filename.split(".")[2] + ".csv"
        utils.raw_to_csv(f, output_file_name, fieldnames)

# Iterate CSV file output from script #1 and use maptouuids() to map and merge data
# which is then outputted to the user specified directory
for filename in os.listdir(csv_out_dir):
    f = os.path.join(csv_out_dir, filename)
    if os.path.isfile(f):
        name = filename.split('.')[0]
        path = map_out_dir + name + "_mapping_output.csv"
        utils.maptouuids(sdpath=f, uuidpath=uuid_file).to_csv(index=False, path_or_buf=path)

