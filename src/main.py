import sys
import argparse
from tools.applications import *
from tools.performance import initPerformanceChenking
from tools.properties import calculateProperties
from tools.benchmark import calculateBenchmark
from simple_chalk import chalk


def graphicsForCheck(cdir, all_args):
    
    if all_args.tmpe or all_args.pres or all_args.teng :
        calculateProperties(cdir, all_args.tmpe, all_args.pres, all_args.teng)


def graphicsForPerformance(cdir, all_args):

    if all_args.tloop or all_args.tper :
        calculateBenchmark(cdir, all_args.tloop, all_args.tper)


current_dirs_parent = os.path.dirname(os.getcwd())

parser = argparse.ArgumentParser()

parser.add_argument("-A", "--account", default="default", help="Account to be charged for resources used")
parser.add_argument("-C", "--constraint", choices=["type_a", "type_b", "type_c", "type_d"], default="type_a", help="Required node features (type of node)")
#parser.add_argument("-c", "--cpus-per-task", type=int, choices=[1,2,4,16], default=1, help="Number of CPUs required per task")
parser.add_argument("-e", "--error", default="error-%j.err", help="File in which to store job error messages (sbatch and srun only)")
#parser.add_argument("--gpus-per-task", type=int, choices=[0,1,2,4], default=0, help="Number of GPUs required per task")
parser.add_argument("-G", "--gpus", type=int, choices=[0,1,2,4], default=0, help="Number of GPUs required per task")
parser.add_argument("-J", "--job-name", default="default", help="Job name")
parser.add_argument("-N", "--nodes", type=int, choices=[1], default=1, help="Number of nodes required for the job")
parser.add_argument("-n", "--ntasks", type=int, choices=[1,2,4,8,16], default=1, help="Number of tasks to be launched (MPI processes)")
#parser.add_argument("--ntasks-per-node", type=int, choices=[1,2,4,8,16], default=1, help="Number of tasks to be launched per node")
parser.add_argument("-o", "--output", default="output-%j.log", help="File in which to store job output (sbatch and srun only)")
parser.add_argument("-t", "--time", default="00:10:00", help="Limit for job run time")
parser.add_argument("--credits", action="store_true", help="About framework")
parser.add_argument("--check", action="store_true", help="Check resources on HPC, genarates and executes batch file for execution")
parser.add_argument("--performance", action="store_true", help="Check resources on HPC for performance benchmark")
parser.add_argument("--automatic", action="store_true", help="Automatic execution for performance and check resources, in this specific order")

parser.add_argument('--tmpe', action='store_true', help="Calculates Average Temperature. Use with 'check' and 'automatic' parameters")
parser.add_argument('--pres', action='store_true', help="Calculates Average Pressure. Use with 'check' and 'automatic' parameters")
parser.add_argument('--teng', action='store_true', help="Calculates Average Total Energy. Use with 'check' and 'automatic' parameters")

parser.add_argument('--tloop', action='store_true', help="Calculates Loop Time. Use with 'performance' and 'automatic' parameters")
parser.add_argument('--tper', action='store_true', help="Calculates Performance. Use with 'performance' and 'automatic' parameters")


args = parser.parse_args()
#print(type(args))
#print(args)

if not len(sys.argv) > 1:
    mainEntry()
else:
    if args.credits:
        showCredits()
    elif args.check:
        
        initCheck(current_dirs_parent, args)
        graphicsForCheck(current_dirs_parent, args)
        print(chalk.bold(f"\nOverall Check for Resources process"), f"........", f"[", chalk.green.bold(f"Finished"), chalk.bold(f"]\n") )

    elif args.performance:

        initPerformanceChenking(current_dirs_parent, args)
        graphicsForPerformance(current_dirs_parent, args)
        print(chalk.bold(f"\nOverall Check Performance process"), f"........", f"[", chalk.green.bold(f"Finished"), chalk.bold(f"]\n") )

    elif args.automatic:

        initPerformanceChenking(current_dirs_parent, args)
        graphicsForPerformance(current_dirs_parent, args)
        print(chalk.bold(f"\nOverall Check Performance process"), f"........", f"[", chalk.green.bold(f"Finished"), chalk.bold(f"]\n") )
        

        initCheck(current_dirs_parent, args)
        graphicsForCheck(current_dirs_parent, args)
        print(chalk.bold(f"\nOverall Check for Resources process"), f"........", f"[", chalk.green.bold(f"Finished"), chalk.bold(f"]\n") )
        

