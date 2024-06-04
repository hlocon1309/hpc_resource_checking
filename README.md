# A software framework for the automatic evaluation of physical properties from atomistic simulations

## Description

Description

## Installation

For cloning the repo just execute:

```
git clone https://github.com/hlocon1309/hpc_resource_checking.git

```
## How to Start

After cloning repo, go to main folder and execute setup script file

```
./setup.sh

```
Then go to source folder, active virtual environment. Run main scritp with -h parameter for help.

```
cd src
. venv/bin/active
python3 main.py -h

```
## Interactive Mode

Interactive mode is intended to generate the input file for LAMMPS package. For interactive mode, apply the following command:

```
python3 main.py --imode

```
## Check Resources

Check Resources executes various steps to check physical resources from HPC system. Using the command “check” without parameters generates a default checking process, but it’s possible that it could fail. It is better to set the parameters needed for a specific check.
```
python3 main.py --check

```
### Paremeters

Parameters for this process and their description are shown below:
```
  -A, --account: Account to be charged for resource check
  -C, --constraint {type_a,type_b,type_c,type_d}: Required node features (type of node)
  -e, --error ERROR: File name to store job error messages (sbatch and srun only)
  -G, --gpus {0,1,2,4}: Number of GPUs required per task
  -J, --job-name JOB_NAME: Job name
  -N, --nodes {1}: Number of nodes required for job execution
  -n, --ntasks {1,2,4,8,16}: Number of tasks to be launched (MPI processes)
  -o, --output OUTPUT: File name to store job output (sbatch and srun only)
  -t, --time TIME: Limit for job run time

```
## Performance

This action can be executed using the command “performance”

```
$ python3 main.py --performance

```
Also it is possible with the command “automatic”, but in this case, application executes check process first.

```
$ python3 main.py --automatic

```
Of course the other commands and parameters are needed, just like the “check” option.

## Data Processing and Visualization

To complete the data processing after simulation and performance test, some command could be used to visualize filtered data. Description for command is shown below:

```
  --tmpe: Calculates Average Temperature. Use with 'check' and 'automatic' parameters
  --pres: Calculates Average Pressure. Use with 'check' and 'automatic' parameters
  --teng: Calculates Average Total Energy. Use with 'check' and 'automatic' parameters

  --tloop: Calculates Loop Time. Use with 'performance' and 'automatic' parameters
  --tper: Calculates Performance. Use with 'performance' and 'automatic' parameters

```
