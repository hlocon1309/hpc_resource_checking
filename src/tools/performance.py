
import os
import time
import configparser
from simple_chalk import chalk
from pssh.clients import SSHClient

from tools.connection import connectionToServer, getCoonnectionParams, executeCommandOnServer
from tools.resources import printGeneralInfo, getAvailableNode
from tools.applications import addToBatchFile, readConfigParams


def initPerformanceChenking(url, all_args):

    print( chalk.yellow.bold( f"\nInitializing Performance Benchmark Procedure" ), chalk.yellow.bold( f"........" ), f"\n" )

    checkRemoteDirectory("check_performance")

    connectionToServer(all_args.constraint, "check_performance/node_performance.txt", "check_performance/filter_node_type.txt", "../node_performance.txt", "../filter_node_type.txt", "check_performance")

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
            addToBatchFile("\n#SBATCH "+"--nodelist="+fixednode, 'a', file_nm)
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

        generateFilters()

        retreivePerformanceLog("check_performance/performance.log", "../performance.log", "check_performance/loop.log", "../loop.log")


def generateFilters():

    host_data = getCoonnectionParams("HOST", "host")
    user_data = getCoonnectionParams("USER", "user")
    password_data = getCoonnectionParams("PASSWORD", "password")
    port_data = getCoonnectionParams("PORT", "port")

    client = SSHClient( host_data, user=user_data, password=password_data, port=int(port_data) )

    executeCommandOnServer(client, "grep Performance check_performance/output* > check_performance/performance.log", "filtering performance")
    executeCommandOnServer(client, "grep Loop check_performance/output* > check_performance/loop.log", "filtering loop time")



def checkRemoteDirectory(directory):
    host_data = getCoonnectionParams("HOST", "host")
    user_data = getCoonnectionParams("USER", "user")
    password_data = getCoonnectionParams("PASSWORD", "password")
    port_data = getCoonnectionParams("PORT", "port")

    client = SSHClient( host_data, user=user_data, password=password_data, port=int(port_data) )

    cmd = """
                if [ -d {0} ]; then
                    rm -r {0}
                fi
                """.format(directory)

    executeCommandOnServer(client, cmd, "cheking if exists '{0}'".format(directory))

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
    
    print( chalk.bold( f"\nWaiting 60 seconds to complete execution" ), chalk.bold( f"........" ) )
    time.sleep(60)
    print( chalk.bold( f"\nExecution finished" ), chalk.bold( f"........" ), f"[", chalk.green.bold(f"OK"), chalk.bold(f"]") )


def retreivePerformanceLog(gen_performance_file, local_performance, gen_loop_file, local_loop ):

    host_data = getCoonnectionParams("HOST", "host")
    user_data = getCoonnectionParams("USER", "user")
    password_data = getCoonnectionParams("PASSWORD", "password")
    port_data = getCoonnectionParams("PORT", "port")

    client = SSHClient( host_data, user=user_data, password=password_data, port=int(port_data) )

    cmds = client.copy_remote_file(gen_performance_file, local_performance)
    cmds = client.copy_remote_file(gen_loop_file, local_loop)

    print(chalk.bold(f"\nCoping performance and loop time results from server"), f"........", f"[", chalk.green.bold(f"OK"), chalk.bold(f"]") )