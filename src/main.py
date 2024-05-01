import sys
import argparse
from tools.applications import *
from simple_chalk import chalk

current_dirs_parent = os.path.dirname(os.getcwd())

parser = argparse.ArgumentParser()

parser.add_argument("-A", "--account", default="default", help="Account to be charged for resources used")
parser.add_argument("-C", "--constraint", choices=["type_a", "type_b", "type_c", "type_d", "type_e"], default="type_a", help="Required node features (type of node)")
#parser.add_argument("-c", "--cpus-per-task", type=int, choices=[1,2,4,16], default=1, help="Number of CPUs required per task")
parser.add_argument("-e", "--error", default="error-%j.err", help="File in which to store job error messages (sbatch and srun only)")
#parser.add_argument("--gpus-per-task", type=int, choices=[0,1,2,4], default=0, help="Number of GPUs required per task")
parser.add_argument("-G", "--gpus", type=int, choices=[0,1,2,4], default=0, help="Number of GPUs required per task")
parser.add_argument("-J", "--job-name", default="default", help="Job name")
parser.add_argument("-N", "--nodes", type=int, choices=[1,2], default=1, help="Number of nodes required for the job")
parser.add_argument("-n", "--ntasks", type=int, choices=[1,2,4,8,16], default=1, help="Number of tasks to be launched (MPI processes)")
#parser.add_argument("--ntasks-per-node", type=int, choices=[1,2,4,8,16], default=1, help="Number of tasks to be launched per node")
parser.add_argument("-o", "--output", default="output-%j.log", help="File in which to store job output (sbatch and srun only)")
parser.add_argument("-t", "--time", default="00:10:00", help="Limit for job run time")
parser.add_argument("--credits", action="store_true", help="About framework")
parser.add_argument("--check", action="store_true", help="Check for resources on HPC, genarates and executes batch file for execution")

args = parser.parse_args()
print(type(args))
print(args)

if not len(sys.argv) > 1:
    mainEntry()
else:
    if args.credits:
        showCredits()
    elif args.check:
        initCheck(current_dirs_parent, args)
    """else:
        addToBatchFile("#!/bin/sh\n", 'a')
        addToBatchFile("\n#SBATCH "+"--account="+args.account, 'a')
        addToBatchFile("\n#SBATCH "+"--constraints="+args.constraints, 'a')
        #addToBatchFile("\n#SBATCH "+"--cpus-per-task="+str(args.cpus_per_task), 'a')
        addToBatchFile("\n#SBATCH "+"--error="+args.error, 'a')
        #addToBatchFile("\n#SBATCH "+"--gpus-per-task="+str(args.gpus_per_task), 'a')
        addToBatchFile("\n#SBATCH "+"--gpus="+str(args.gpus), 'a')
        addToBatchFile("\n#SBATCH "+"--job-name="+args.job_name, 'a')
        addToBatchFile("\n#SBATCH "+"--nodes="+str(args.nodes), 'a')
        addToBatchFile("\n#SBATCH "+"--ntasks="+str(args.ntasks), 'a')
        #addToBatchFile("\n#SBATCH "+"--ntasks-per-node="+str(args.ntasks_per_node), 'a')
        addToBatchFile("\n#SBATCH "+"--output="+args.output, 'a')
        addToBatchFile("\n#SBATCH "+"--time="+args.time, 'a')
        addToBatchFile("\n\nmodule purge", 'a')
        addToBatchFile("\nmodule load "+readConfigParams("MODULE"), 'a')
        addToBatchFile("\nsrun "+readConfigParams("SRUN"), 'a')
        addToBatchFile(" "+readConfigParams("INPUTFILE"), 'a')
    """


    

"""
#!/bin/bash
#SBATCH --job-name={task}            # Job name
#SBATCH --error={task}-%j.err        # File for outputting error
#SBATCH --output={task}-%j.log       # File for outputting results
#SBATCH --time={12:00:00}            # Maximum execution time
#SBATCH --ntasks={16}                # Number of MPI processes
#SBATCH --nodes={1}                  # Required number of nodes
#SBATCH --gpus={4}                   # Required GPU
#SBATCH --cpus-per-task={2}  
"""

"""
#!/bin/sh
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -p normal
#SBATCH -A proj_1460
#SBATCH --time=00:30:00
#SBATCH --constraint=type_b

module purge
module load openmpi/4.1.4
module load CUDA/11.7
module load lammps/2022jun23_update1

srun --mpi=pmix_v2 lmp -i in.lj

"""




"""

#!/bin/sh
#SBATCH -N 1
#SBATCH -n 16
#SBATCH -p normal
#SBATCH --nodelist=cn-[017]
#SBATCH --gpus=2
#SBATCH -A proj_1371
#SBATCH --constraint=type_b

module load openmpi/4.1.4
module load CUDA/11.7
module load lammps/2022jun23_update1

srun --mpi=pmix_v2 lmp -i in.lj -sf gpu -pk gpu 2

"""

"""

#!/bin/sh
#SBATCH -N 2
#SBATCH -n 16
#SBATCH -p normal
#SBATCH --nodelist=cn-[017,018]
#SBATCH --gpus-per-node=2
#SBATCH -A proj_1371
#SBATCH --constraint=type_b

module load openmpi/4.1.4
module load CUDA/11.7
module load lammps/2022jun23_update1

srun --mpi=pmix_v2 lmp -i in.lj -sf gpu -pk gpu 2


"""