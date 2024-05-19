import os
import configparser
from simple_chalk import chalk
from tools.connection import connectionToServer, copyBatchToServer, retreiveOutuputLog
from tools.resources import printGeneralInfo, getAvailableNode

def mainEntry():
    print(chalk.green.bold("\nHPC Resource Checking\n"))
    print(chalk.red.bold("A software framework for real-time resource checking and automatic batch file generation and execution\n"))
    print(chalk.yellow.bold("Please run the aplication and specify the needed parameters, -h for help.\n"))


def showCredits():
    print(chalk.green.bold(f"\n>>> CREDITS <<<\n"))
    print(f"\t", chalk.green.bold(f">>> "), chalk.bold(f"Rufino Haroldo Locon"), f"\t\t", f"Main Developer\n")
1

def initCheck(url, all_args):

    print(chalk.yellow.bold(f"\nInitializing Resource Check Procedure"), f"........", f"\n")

    connectionToServer(all_args.constraint,"check_resources/free_nodes.txt", "check_resources/filter_nodes.txt", "../free_nodes.txt", "../filter_nodes.txt", "check_resources")
    printGeneralInfo(url, "/filter_nodes.txt")
    rnode = getAvailableNode(url, "/filter_nodes.txt", all_args.ntasks, all_args.gpus)

    if ( rnode == "unavailable" ):
        print( chalk.red.bold(f"\nError: could not create batch file due to lack of resources") )
    else:
        file_nm = "/simulation/job.sh"
        addToBatchFile("#!/bin/sh\n", 'w', file_nm)
        addToBatchFile("\n#SBATCH "+"--account="+all_args.account, 'a', file_nm)
        addToBatchFile("\n#SBATCH "+"--job-name="+all_args.job_name, 'a', file_nm)
        addToBatchFile("\n#SBATCH "+"--constraint="+all_args.constraint, 'a', file_nm)
        addToBatchFile("\n#SBATCH "+"--nodes="+str(all_args.nodes), 'a', file_nm)
        addToBatchFile("\n#SBATCH "+"--ntasks="+str(all_args.ntasks), 'a', file_nm)
        if not ( all_args.gpus == 0 ) :
            addToBatchFile("\n#SBATCH "+"--gpus="+str(all_args.gpus), 'a', file_nm)
        splitnode = rnode.split("-")
        fixednode = splitnode[0] + "-" + "[" + splitnode[1] + "]"
        addToBatchFile("\n#SBATCH "+"--nodelist="+fixednode, 'a', file_nm)
        addToBatchFile("\n#SBATCH "+"--output="+"output.log", 'a', file_nm) ### all_args.output
        addToBatchFile("\n#SBATCH "+"--error="+"error.err", 'a', file_nm)  ### all_args.error
        addToBatchFile("\n#SBATCH "+"--time="+all_args.time, 'a', file_nm)
        addToBatchFile("\n\nmodule purge", 'a', file_nm)
        addToBatchFile("\nmodule load "+readConfigParams("MODULE", "openmpi"), 'a', file_nm)
        addToBatchFile("\nmodule load "+readConfigParams("MODULE", "cuda"), 'a', file_nm)
        addToBatchFile("\nmodule load "+readConfigParams("MODULE", "lammps"), 'a', file_nm)
        srun = readConfigParams("SRUN", "srun")
        if ( all_args.gpus > 0 ) :
            srun += " -sf gpu -pk gpu "
            srun += str( all_args.gpus )
        addToBatchFile("\nsrun "+srun, 'a', file_nm)
        
        addToBatchFile(" "+readConfigParams("INPUTFILE", "inputfile"), 'a', file_nm)
        print( chalk.bold(f"\nBatch file created"), f"........", f"[", chalk.green.bold(f"OK"), chalk.bold(f"]" ) )
        copyBatchToServer("simulation", "check_resources")

        retreiveOutuputLog("check_resources/output.log", "../output.log")


def addToBatchFile(text, mode, file_name):
    try:
        current_dirs_parent = os.path.dirname(os.getcwd())
        #print(current_dirs_parent)
        with open(current_dirs_parent + file_name, mode) as f:
            f.write(text)
    except IOError:
        print(chalk.red.bold(f"Error: could not create file"))


def readConfigParams(parameter, subparam):

    config = configparser.ConfigParser()

    try:
        current_dirs_parent = os.path.dirname(os.getcwd())
        config.read(current_dirs_parent + "/config/params.conf")
        param = config.get(parameter, subparam)
        
        return param

    except IOError:
        print(chalk.red.bold(f"Error: could not open configuration file"))
    