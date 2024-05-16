

# Estrategia:
# 

# 1 -> Standard input file, specific for LAMMPS and with large number of atoms
#   --> Find old files - DONE

# 2 -> Node type, default a, default 16 cores, 0 gpus
#   --> Check for node number, if available - DONE

# 3 -> check for resources, if gpus not available, specify that performances is running only in cpus
#   --> Using procedures from resources - "getAvailableNode" - DONE

# 4 -> from above, generate batch files for 1, 2, 4, 8 and 16 cores (tasks)
#   --> ? - DONE, DONE, DONE

# 5 -> send to de queue on HPC (execute)
#   --> Tested with one file, still tests with bench pool
#   --> Tested with 5 files - DONE

# 6 -> every second check the current user's queue, and determine the completed porcentage
#   --> Descartar este paso de momento - aplicar un sleep de 30 segundos

# 7 -> when completed check generated files, filter performance and walltime
#   --> \ | / _

# -> generate graphics for performance and walltime


 ##### ---------------------------------------------------------------------------

import os
import time
import configparser
from simple_chalk import chalk
from pssh.clients import SSHClient

from tools.connection import connectionToServer, getCoonnectionParams
from tools.resources import printGeneralInfo, getAvailableNode
from tools.applications import addToBatchFile, readConfigParams


def initPerformanceChenking(url, all_args):

    print( chalk.yellow.bold( f"\nInitializing Performance Benchmark Procedure" ), chalk.yellow.bold( f"........" ), f"\n" )

    connectionToServer("type_a", "check_performance/node_performance.txt", "check_performance/filter_node_type.txt", "../node_performance.txt", "../filter_node_type.txt", "check_performance")

    printGeneralInfo(url, "/filter_node_type.txt")

    rnode = getAvailableNode(url, "/filter_node_type.txt", 16, 0)

    if ( rnode == "unavailable" ):
        print( chalk.red.bold(f"\nError: could not create batch file due to lack of resources") )
    else:
        cores = [1, 2, 4, 8, 16]
        for core in cores:
            file_nm = "/performance/test_{0}.sh".format(core)
            addToBatchFile("#!/bin/sh\n", 'w', file_nm)
            addToBatchFile("\n#SBATCH "+"--account="+all_args.account, 'a', file_nm)
            addToBatchFile("\n#SBATCH "+"--job-name="+all_args.job_name, 'a', file_nm)
            addToBatchFile("\n#SBATCH "+"--constraint="+all_args.constraint, 'a', file_nm)
            addToBatchFile("\n#SBATCH "+"--nodes="+str(all_args.nodes), 'a', file_nm)
            addToBatchFile("\n#SBATCH "+"--ntasks="+str(core), 'a', file_nm)
            if not ( all_args.gpus == 0 ) :
                addToBatchFile("\n#SBATCH "+"--gpus="+str(all_args.gpus), 'a', file_nm)
            splitnode = rnode.split("-")
            fixednode = splitnode[0] + "-" + "[" + splitnode[1] + "]"
            addToBatchFile("\n#SBATCH "+"--nodelist="+fixednode, 'a', file_nm) #### SBATCH --nodelist=cn-[017]
            addToBatchFile("\n#SBATCH "+"--output="+all_args.output, 'a', file_nm)
            addToBatchFile("\n#SBATCH "+"--error="+all_args.error, 'a', file_nm)
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
            
            addToBatchFile(" "+readConfigParams("BENCHFILE", "benchfile"), 'a', file_nm)

        print( chalk.bold(f"\nPerformance Bechmark batch file pool created"), f"........", f"[", chalk.green.bold(f"OK"), chalk.bold(f"]" ) )
        copyBatchToServer("performance", "check_performance")


def copyBatchToServer(local_dir, remote_dir):

    host_data = getCoonnectionParams("HOST", "host")
    user_data = getCoonnectionParams("USER", "user")
    password_data = getCoonnectionParams("PASSWORD", "password")
    port_data = getCoonnectionParams("PORT", "port")

    client = SSHClient( host_data, user=user_data, password=password_data, port=int(port_data) )
    
    bench = [1, 2, 4, 8, 16]
    
    cmds = client.copy_file("../{0}/in.lj".format(local_dir), "{0}/in.lj".format(remote_dir))
    print( chalk.bold(f"Coping Testing File in.lj"), f"........", f"[", chalk.green.bold(f"OK"), chalk.bold(f"]") )

    for nb in bench:

        cmds = client.copy_file("../{0}/test_{1}.sh".format(local_dir, nb), "{0}/test_{1}.sh".format(remote_dir, nb))
        print( chalk.bold("\nCoping test_{0}.sh".format(nb)), f"........", f"[", chalk.green.bold(f"OK"), chalk.bold(f"]") )

        cmd = """cd {0}
                sbatch test_{1}.sh""".format(remote_dir, nb)
        host_out = client.run_command(cmd)
        print( chalk.bold( f"\nExecuting job" ), chalk.bold( f"........" ) )
        for line in host_out.stdout:
            print(f"\t", chalk.green.bold(line) )
        for line in host_out.stderr:
            print(f"\t", chalk.red.bold(line) )

        time.sleep(1)


##########################################################################################


"""
output-\d{7}.log:Loop time of 


output-1956448.log:Loop time of 36.2733 on 1 procs for 1000 steps with 64000 atoms
output-1956449.log:Loop time of 20.1469 on 2 procs for 1000 steps with 64000 atoms
output-1956450.log:Loop time of 10.4762 on 4 procs for 1000 steps with 64000 atoms
output-1956451.log:Loop time of 5.61517 on 8 procs for 1000 steps with 64000 atoms
output-1956452.log:Loop time of 2.93171 on 16 procs for 1000 steps with 64000 atoms

(output-[0-9]+[.]log:Loop time of )|( on )|( procs for )|( steps with )|( atoms)

36.2733 on 1 procs for 1000 steps with 64000 atoms
20.1469 on 2 procs for 1000 steps with 64000 atoms
10.4762 on 4 procs for 1000 steps with 64000 atoms
5.61517 on 8 procs for 1000 steps with 64000 atoms
2.93171 on 16 procs for 1000 steps with 64000 atoms


---------------------------------------------------------------------------------

"""





###########################################################################################

"""
def connectToServer(constraints):

    host_data = getCoonnectionParams("HOST", "host")  #'cluster.hpc.hse.ru'
    user_data = getCoonnectionParams("USER", "user")
    password_data = getCoonnectionParams("PASSWORD", "password")
    port_data = getCoonnectionParams("PORT", "port")

    client = SSHClient( host_data, user=user_data, password=password_data, port=int(port_data) )

    executeCommandOnServer(client, "mkdir check_performance", "creating directory 'check_resources'")
    executeCommandOnServer(client, "freenodes -d > check_performance/node_performance.txt", "retrieving resource info")
    executeCommandOnServer(client, "grep {0} check_performance/node_performance.txt > check_performance/filter_node_type.txt".format(constraints), "filtering based on node type")

    copyFilesFromServer(client)

    print(chalk.bold(f"Checking resources from node"), f"........", "[ ", chalk.green.bold(constraints), " ]\n" )
"""


"""
def copyFilesFromServer(cliente):

    cmds = cliente.copy_remote_file('check_performance/node_performance.txt', '../node_performance.txt')
    print(chalk.bold(f"Coping freenodes data from server"), f"........", f"[", chalk.green.bold(f"OK"), chalk.bold(f"]") )
    
    cmds = cliente.copy_remote_file('check_performance/filter_node_type.txt', '../filter_node_type.txt')
    print(chalk.bold(f"Coping filtered data from server"), f"........", f"[", chalk.green.bold(f"OK"), chalk.bold(f"]") )
""" 


"""   
def executeCommandOnServer(cliente, command, message): #executeCommandOnServer("mkdir check_resources", "creating directory 'check_resources'")

    host_out = cliente.run_command(command)
    error_message = ""
    success = chalk.green.bold(f"OK")
    has_error = False
    for line in host_out.stderr:
        error_message += str( line )
        has_error = True
    if has_error:
        success = chalk.red.bold(f"FAILED")

    print(f"\t", chalk.yellow.bold(f">>> "), chalk.bold(message), f"........", f"[", success, chalk.bold(f"]"))
    if not ( error_message == "" ):
        print( f"\t\t", chalk.red.bold(error_message ) )
    time.sleep(0.1)
"""


"""
def generateBatchFiles(url, all_args):
    
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
"""