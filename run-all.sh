#! /usr/bin/env bash

# positional params put here later
PARAMS=""

# default values
PROJECTDIR=~/Developer/student-projects/testsubs
TASKFILE=tasks.json
STEPS=""
SKIP_TASKS=false
SKIP_RUN=false
DEPTH=1

showhelp () {
  echo "Positional arguments (should be in this relative order):"
  echo -e "\tPROJECTDIR: The directory containing submissions to be mutated."
  echo -e "\t\tDefaults to ${PROJECTDIR}"
  echo -e "\tTASKFILE: The file to which tasks for GNU Parallel should be written."
  echo -e "\t\tDefaults to ${TASKFILE}"
  echo "Named arguments:"
  echo -e "\t-d --find-depth: Exact depth at which to find directories to mutate, within PROJECTDIR"
  echo "Options:"
  echo -e "\t-s: Run testing with one mutation operator at a time?"
  echo -e "\t-t: Skip generating a task file? Use this if you already have tasks written to a file."
  echo -e "\t-r: Skip mutation testing? Convenient to only write tasks."
}

while (( "$#" )); do
  case "$1" in
    -t)
      SKIP_TASKS=true
      shift
      ;;
    -r)
      SKIP_RUN=true
      shift
      ;;
    -s)
      STEPS="-s"
      shift
      ;;
    -d|--find-depth) DEPTH=$2
      shift 2
      ;;
    -h|--help)
      showhelp
      exit 0
      ;;
    --) # end argument parsing
      shift
      break
      ;;
    *) # preserve positionals
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done

eval set -- "$PARAMS" 

if [[ -n "$1" ]]; then
  PROJECTDIR=$1
fi

if [[ -n "$2" ]]; then
  TASKFILE=$2
fi 

if [ "$SKIP_TASKS" = false ] ; then 
  rm -f ${TASKFILE}
  find  ${PROJECTDIR} -maxdepth ${DEPTH} -mindepth ${DEPTH} -type d | while read line; do
    echo "{ \"projectPath\": \"$line\", \"antTask\": \"pit\" }" >> $TASKFILE
  done
  echo "Wrote tasks from ${PROJECTDIR} to ${TASKFILE}."
fi

if [ "$SKIP_RUN" = false ] ; then
  echo "Starting mutation testing. This might take a while."
  ./run_mutation_test.py ${TASKFILE} ${STEPS} > /tmp/mutation-results.json
  echo "FINISHED"
  echo -e "\tRun summary in /tmp/mutation-results.json"
  echo -e "\tPITest reports in /tmp/mutation-testing/."
  echo -e "\tUse ./aggregrate_results.py to translate PIT reports to coverage data."
fi 
