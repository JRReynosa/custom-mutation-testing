# custom-mutation-testing

Scripts cloned from [mutation-testing](https://github.com/ayaankazerouni/mutation-testing) to run mutation analysis on collections of student submissions to programming assignments. This fork is meant for edits to the PIT mutation testing.

Mutation testing tools enabled:
* PIT
* \[EXPERIMENTAL\] muJava (See [mutation-testing](https://github.com/ayaankazerouni/mutation-testing))

## Overview
### [PIT](https://pitest.org)

Usage: [`./pit_runner.py --help`](pit/pit_runner.py)

[pit/pit-runner.py](pit/pit_runner.py) run PIT with different possible sets of operators:
* `default` set (according to PIT website)
* our approximation of Offutt's `deletion` set 
* our approximation of Offutt's `sufficient` set
* `all` PIT operators evaluated in Laurent et al.'s 2017 paper
* a custom set of operators, provided as CLI arguments

### [analysis](analysis)
See [mutation-testing](https://github.com/ayaankazerouni/mutation-testing)

### Utilities
See [mutation-testing](https://github.com/ayaankazerouni/mutation-testing)

### **EXPERIMENTAL** [muJava](https://cs.gmu.edu/~offutt/mujava/)
See [mutation-testing](https://github.com/ayaankazerouni/mutation-testing)
