
import os
import configparser
from simple_chalk import chalk


def setCredentials():

    print(chalk.cyan.bold(f'>>> SET CONNECTION CREDENTIALS <<<\n'))


    #host - cluster.hpc.hse.ru
    host = input(chalk.bold(f'Enter parameter for host: [unknown] '))
    if host:
        setConfigurationParams("HOST", "host", host)
    else:
        setConfigurationParams("HOST", "host", "unknown")
    
    #user - rloconamezquita
    user = input(chalk.bold(f'Enter parameter for user: [unknown] '))
    if user:
        setConfigurationParams("USER", "user", user)
    else:
        setConfigurationParams("USER", "user", "unknown")
    
    #password - Microsistem@s001
    password = input(chalk.bold(f'Enter parameter for password: [unknown] '))
    if password:
        setConfigurationParams("PASSWORD", "password", password)
    else:
        setConfigurationParams("PASSWORD", "password", "unknown")
    
    #port - 2222
    port = input(chalk.bold(f'Enter parameter for port: [unknown] '))
    if port:
        setConfigurationParams("PORT", "port", port)
    else:
        setConfigurationParams("PORT", "port", "unknown")



def setConfigurationParams(parameter, subparam, credential):

    config = configparser.ConfigParser()

    try:
        current_dirs_parent = os.path.dirname(os.getcwd())
        config.read(current_dirs_parent + "/config/params.conf")
        config.set(parameter, subparam, credential)

        with open(current_dirs_parent + "/config/params.conf", 'w') as configfile:
            config.write(configfile)

    except IOError:
        print(chalk.red.bold(f"Error: could not open configuration file"))