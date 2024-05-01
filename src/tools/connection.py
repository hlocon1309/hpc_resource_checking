import os
import time
import configparser
from simple_chalk import chalk
from pssh.clients import SSHClient


def connectionToServer(constraints):

    host_data = getCoonnectionParams("HOST", "host")  #'cluster.hpc.hse.ru'
    user_data = getCoonnectionParams("USER", "user")
    password_data = getCoonnectionParams("PASSWORD", "password")
    port_data = getCoonnectionParams("PORT", "port")

    #client = SSHClient(host_data, user='rloconamezquita', password='Microsistem@s001', port=2222)
    client = SSHClient( host_data, user=user_data, password=password_data, port=int(port_data) )

    #cmd = """mkdir check_resources
    #        cd check_resources
    #        freenodes -d > free_nodes.txt
    #        grep {0} free_nodes.txt > filter_nodes.txt
    #        echo 'executing ..... '""".format(constraints)

    #host_out = client.run_command(cmd)


    executeCommandOnServer(client, "mkdir check_resources", "creating directory 'check_resources'")
    #executeCommandOnServer(client, "cd check_resources", "entering directory 'check_resources'")
    executeCommandOnServer(client, "freenodes -d > check_resources/free_nodes.txt", "retrieving resource info")
    executeCommandOnServer(client, "grep {0} check_resources/free_nodes.txt > check_resources/filter_nodes.txt".format(constraints), "filtering based on node type")

    copyFilesFromServer(client)

    print(chalk.bold(f"Checking resources from node"), f"........", "[ ", chalk.green.bold(constraints), " ]\n" )


def copyFilesFromServer(cliente):

    cmds = cliente.copy_remote_file('check_resources/free_nodes.txt', '../free_nodes.txt')
    print(chalk.bold(f"Coping freenodes data from server"), f"........", f"[", chalk.green.bold(f"OK"), chalk.bold(f"]") )
    
    cmds = cliente.copy_remote_file('check_resources/filter_nodes.txt', '../filter_nodes.txt')
    print(chalk.bold(f"Coping filtered data from server"), f"........", f"[", chalk.green.bold(f"OK"), chalk.bold(f"]") )
    
    
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


def copyBatchOnServer():

    host_data = getCoonnectionParams("HOST", "host")
    user_data = getCoonnectionParams("USER", "user")
    password_data = getCoonnectionParams("PASSWORD", "password")
    port_data = getCoonnectionParams("PORT", "port")

    client = SSHClient( host_data, user=user_data, password=password_data, port=int(port_data) )
    
    cmds = client.copy_file('../simulation/job.sh', 'check_resources/job.sh')
    print( chalk.bold(f"\nCoping job.sh"), f"........", f"[", chalk.green.bold(f"OK"), chalk.bold(f"]") )

    cmds = client.copy_file('../simulation/params.in', 'check_resources/params.in')
    print( chalk.bold(f"Coping params.in"), f"........", f"[", chalk.green.bold(f"OK"), chalk.bold(f"]") )

    cmd = """cd check_resources
             sbatch job.sh"""
    host_out = client.run_command(cmd)
    print( chalk.bold( f"\nExecuting job", f"........" ) )
    for line in host_out.stdout:
        print(f"\t", chalk.green.bold(line) )
    for line in host_out.stderr:
        print(f"\t", chalk.red.bold(line) )


def getCoonnectionParams(parameter, subparam):

    config = configparser.ConfigParser()

    try:
        current_dirs_parent = os.path.dirname(os.getcwd())
        config.read(current_dirs_parent + "/config/params.conf")
        param = config.get(parameter, subparam)
        
        return param

    except IOError:
        print(chalk.red.bold(f"Error: could not open configuration file"))