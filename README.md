# custom-mutation-testing

Scripts cloned from [mutation-testing](https://github.com/ayaankazerouni/mutation-testing) to run mutation analysis on collections of student submissions to programming assignments. This fork is meant for edits to the PIT mutation testing.

Mutation testing tools enabled:
* PIT
* \[EXPERIMENTAL\] muJava (See [mutation-testing](https://github.com/ayaankazerouni/mutation-testing))

## Overview
### [PIT](https://pitest.org)

Usage: [`./pit_runner.py --help`](pit/pit_runner.py)

[pit/pit-runner.py](pit/pit_runner.py) run PIT with different possible sets of operators.

To run PIT:
1. In the "custom-mutation-testing" directory, use the write_tasks.py script to create the ndjson file with all paths to the submissions.  
`python3 ./write_tasks.py ~\Project-1 > tasks.ndjson`  
Where Project-1 contains multiple student directories and each student directory contains multiple submissions. The following is the structure: {studentDirectory}/{submissionNumber}/{src}/{*.java}

2. Move the generated tasks.ndjson file into the "custom-mutation-test/pit" directory.

3. In the "custom-mutation-test/pit" directory, use the clone-projects.py script to clone all submissions:    
`python3 ./clone-projects.py tasks.ndjson -p`  
The script creates a "/tmp" and creates the package structure for all submissions.

4. Finally, run PIT.  
`python3 ./pit-runner.py -m custom -l tasks.ndjson > log.txt`

### [analysis](analysis)
See [mutation-testing](https://github.com/ayaankazerouni/mutation-testing)

### Utilities
See [mutation-testing](https://github.com/ayaankazerouni/mutation-testing)

### **EXPERIMENTAL** [muJava](https://cs.gmu.edu/~offutt/mujava/)
See [mutation-testing](https://github.com/ayaankazerouni/mutation-testing)
