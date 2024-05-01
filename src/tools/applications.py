import os
import configparser
from simple_chalk import chalk
from tools.connection import connectionToServer, copyBatchOnServer
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
    print(chalk.yellow.bold(f"\nInitializing Check Procedure", f"........", f"\n"))
    connectionToServer(all_args.constraint)
    printGeneralInfo(url)
    rnode = getAvailableNode(url, all_args.ntasks, all_args.gpus)
    if ( rnode == "unavailable" ):
        print( chalk.red.bold(f"\nError: could not create batch file due to lack of resources") )
    else:
        addToBatchFile("#!/bin/sh\n", 'w')
        addToBatchFile("\n#SBATCH "+"--account="+all_args.account, 'a')
        addToBatchFile("\n#SBATCH "+"--job-name="+all_args.job_name, 'a')
        addToBatchFile("\n#SBATCH "+"--constraint="+all_args.constraint, 'a')
        addToBatchFile("\n#SBATCH "+"--nodes="+str(all_args.nodes), 'a')
        addToBatchFile("\n#SBATCH "+"--ntasks="+str(all_args.ntasks), 'a')
        if not ( all_args.gpus == 0 ) :
            addToBatchFile("\n#SBATCH "+"--gpus="+str(all_args.gpus), 'a')
        splitnode = rnode.split("-")
        fixednode = splitnode[0] + "-" + "[" + splitnode[1] + "]"
        addToBatchFile("\n#SBATCH "+"--nodelist="+fixednode, 'a') #### SBATCH --nodelist=cn-[017]
        addToBatchFile("\n#SBATCH "+"--output="+all_args.output, 'a')
        addToBatchFile("\n#SBATCH "+"--error="+all_args.error, 'a')
        addToBatchFile("\n#SBATCH "+"--time="+all_args.time, 'a')
        addToBatchFile("\n\nmodule purge", 'a')
        addToBatchFile("\nmodule load "+readConfigParams("MODULE", "openmpi"), 'a')
        addToBatchFile("\nmodule load "+readConfigParams("MODULE", "cuda"), 'a')
        addToBatchFile("\nmodule load "+readConfigParams("MODULE", "lammps"), 'a')
        srun = readConfigParams("SRUN", "srun")
        if ( all_args.gpus > 0 ) :
            srun += " -sf gpu -pk gpu "
            srun += str( all_args.gpus )
        addToBatchFile("\nsrun "+srun, 'a')
        
        addToBatchFile(" "+readConfigParams("INPUTFILE", "inputfile"), 'a')
        print( chalk.bold(f"\nBatch file created"), f"........", f"[", chalk.green.bold(f"OK"), chalk.bold(f"]" ) )
        copyBatchOnServer()


def addToBatchFile(text, mode):
    try:
        current_dirs_parent = os.path.dirname(os.getcwd())
        #print(current_dirs_parent)
        with open(current_dirs_parent + "/simulation/job.sh", mode) as f:
            f.write(text)
    except IOError:
        print(chalk.red.bold(f"Error: could not create file"))


def readConfigParams(parameter, subparam):

    config = configparser.ConfigParser()

    try:
        current_dirs_parent = os.path.dirname(os.getcwd())
        config.read(current_dirs_parent + "/config/params.conf")
        #config.readfp(open(r'param.conf'))
        param = config.get(parameter, subparam)
        
        return param
        #path2 = config.get('My Section', 'path2')
        #path3 = config.get('My Section', 'path3')

    except IOError:
        print(chalk.red.bold(f"Error: could not open configuration file"))
    