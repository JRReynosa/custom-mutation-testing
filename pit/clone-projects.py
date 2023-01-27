#! /c/Users/jonny/anaconda3/python
"""Simple utility for cloning projects for mutation testing."""
import os
import sys
import glob
import json
import logging
from shutil import rmtree, copytree
import subprocess
from zipfile import ZipFile
import shutil
from pathlib import Path

def remove_non_ascii(filepath):
    cmd = "perl -pi -e 's/[^[:ascii:]]//g' {}".format(filepath)
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    result.check_returncode()

def clone_project(projectpath, clonepath, package=True):
    """Copy the project at projectpath to the specified clonepath.

    Args:
        projectpath (str): Original path to the initial project
        clonepath (str): Path to be cloned to
        package (bool): Should com.example.* package structure be created?
                        This is needed for PIT testing, so that PIT doesn't
                        try to mutate itself.
    """
    # Copy the project to /tmp/ to avoid modifying the original
    if os.path.exists(clonepath) and os.path.isdir(clonepath):
        rmtree(clonepath)
    copytree(projectpath, clonepath)

    # Example Data
    # clonepath = \tmp\mutation-testing\<PID>
    # \tmp\mutation-testing\<PID>\<Submission #>
    # Up to 100 submissions

    # For each submission in student PID directory
    # i.e. \tmp\mutation-testing\<PID>\1, \tmp\mutation-testing\<PID>\2, etc.

    # Pre-processing here with .zip files
    # If .zip file in directory, unzip the file
    zipfiles = glob.glob(os.path.join(clonepath, '**', '*.zip'), recursive=True)
    for zipfile in zipfiles:
        with ZipFile(zipfile, 'r') as zip_ref:
            zip_ref.extractall(clonepath)

    # Check if src directory already exists, if not then create it.
    src = os.path.join(clonepath, "src")
    if not os.path.isdir(src):
        os.makedirs(src)
        
    # Move source files to src directory
    javafiles = glob.glob(os.path.join(clonepath, '**', '*.java'), recursive=True)
    for javafile in javafiles:
        remove_non_ascii(javafile)
        if not Path(os.path.join(src, os.path.basename(javafile))).exists():
            shutil.move(javafile, src)

    # Delete Everything but the src directory
    for item in os.listdir(clonepath):
        if item != "src":
            item_path = os.path.join(clonepath, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
    
    if package:
        # Create com.example package structure
        pkg = os.path.join(clonepath, 'src', 'com', 'example', '')
        os.makedirs(pkg)

        # Move Java files directly under src into src/com/example
        mvcmd = "mv {javafiles} {package}" \
                .format(javafiles=os.path.join(clonepath, 'src', '*.java'), package=pkg)
        print(mvcmd)
        try:
            result = subprocess.run(mvcmd, shell=True, stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
            result.check_returncode()
        except:
            logging.error(('Could not create com.example package structure for '
                            'project at {}').format(projectpath))
            if result.stdout: logging.error(result.stdout)
            if result.stderr: logging.error(result.stderr)

        # Add package declaration to the top of Java files
        sedcmd = 'gsed' if sys.platform == 'darwin' else 'sed' # requires GNU sed on macOS
        sedcmd = sedcmd + " -i '1ipackage com.example;' {javafiles}" \
                .format(javafiles=os.path.join(pkg, '*.java'))
        try:
            result = subprocess.run(sedcmd, shell=True, stdin=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            result.check_returncode()
        except subprocess.CalledProcessError as err:
            if err.returncode == 127 and sys.platform == 'darwin':
                logging.error(('If you are on macOS, please install the GNU '
                            'sed extension "gsed". To install: brew install gsed'))
                sys.exit(0)
            else:
                logging.error('Could not clone project from {}'.format(projectpath))
                if result.stdout: logging.error(result.stdout)
                if result.stderr: logging.error(result.stderr)

if __name__ == '__main__':
    ARGS = sys.argv[1:]
    if not ARGS:
        print('Error! No args')
        sys.exit(1)
    
    logging.basicConfig(filename='.log-clone', filemode='w', level=logging.WARN)

    outerdir = os.getcwd() + os.path.join('\\', 'tmp', 'mutation-testing')
    if os.path.exists(outerdir) and os.path.isdir(outerdir):
        rmtree(outerdir)

    taskfile = ARGS[0]
    package = '-p' in ARGS
    with open(taskfile, encoding="utf-16") as infile:
        for task in infile:
            opts = json.loads(task)
            projectpath = opts['projectPath']
            clonepath = os.path.join(outerdir, os.path.basename(os.path.split(projectpath)[0]), os.path.basename(projectpath))
            clone_project(projectpath, clonepath, package=package)
