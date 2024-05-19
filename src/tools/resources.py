
import os
import re
from simple_chalk import chalk


def getNode(node_type: str) -> str:
    nod = node_type.lstrip().rstrip()
    nodetype = "[ " + nod + " ]"
    nodef = nod
    return nodetype

def getCPU(cpu_data: str) -> str:
    cpud = cpu_data.lstrip().rstrip().split(" ")
    porcentcpu = float(cpud[1]) / float(cpud[2])
    progress = int( ( porcentcpu ) * 20 )

    def progressBar(places: int) -> str:
        progstr = ""
        for num in range(places):
            progstr +=  "█"
        for num in range(20 - places):
            progstr += "-"
        if int( porcentcpu * 100) <= 25:
            return chalk.red.bold(progstr)
        if ( int( porcentcpu * 100 ) > 25 ) and ( int( porcentcpu * 100 ) <= 75 ):
            return chalk.yellow.bold(progstr)
        if int( porcentcpu * 100 ) > 75:
            return chalk.green.bold(progstr)
    
    def procentUse(porcent: float) -> str:
        porstr = str( int( porcent * 100)  ) + f"%" #porcentage with no decimals
        if int( porcent * 100) < 10:
            porstr = "  " + porstr
        if ( int( porcent * 100) >= 10 ) and ( int( porcent * 100) < 100 ):
            porstr = " " + porstr
        return porstr

    freecpu = cpud[1]
    if int(cpud[1]) < 10:
        freecpu = " " + freecpu
    usecpu = "[ " + cpud[0] + " |" + progressBar(progress) + "| " + procentUse(porcentcpu) + " - " + freecpu + "/" + cpud[2] + " ]"
    return usecpu


def getGPU(gpu_data: str) -> str:
    usegpu = ""
    porcentgpu = 0.0
    gpud = gpu_data.lstrip().rstrip().split(" ")

    if len(gpud) == 2:
        if gpud[1] == "ет":
            usegpu = "[ GPU unavailable ]"
    
    if len(gpud) == 3:
        nodeg = int(gpud[1])
        porcentgpu = float(gpud[1]) / float(gpud[2])
        progress = int( ( porcentgpu ) * 20 )

        def progressBar(places: int) -> str:
            progstr = ""
            for num in range(places):
                progstr +=  "█"
            for num in range(20 - places):
                progstr += "-"
            if int( porcentgpu * 100) <= 25:
                return chalk.red.bold(progstr)
            if ( int( porcentgpu * 100 ) > 25 ) and ( int( porcentgpu * 100 ) <= 75 ):
                return chalk.yellow.bold(progstr)
            if int( porcentgpu * 100 ) > 75:
                return chalk.green.bold(progstr)
        
        def procentUse(porcent: float) -> str:
            porstr = str( int( porcent * 100)  ) + f"%" #porcentage with no decimals
            if int(porcent * 100) < 10:
                porstr = "  " + porstr
            if ( int(porcent * 100) >= 10 ) and ( int(porcent) < 100 ):
                porstr = " " + porstr
            return porstr

        usegpu = "[ " + gpud[0] + " |" + progressBar(progress) + "| " + procentUse(porcentgpu) + " - " + gpud[1] + "/" + gpud[2] + " ]"

    return usegpu


def getRAM(ram_data: str) -> str:
    useram = ""
    ramd = ram_data.lstrip().rstrip().split(" ")
    porcentram = float(ramd[1]) / float(ramd[3])

    progress = int( ( porcentram ) * 20 )

    def progressBar(places: int) -> str:
            progstr = ""
            for num in range(places):
                progstr +=  "█"
            for num in range(20 - places):
                progstr += "-"
            if int( porcentram * 100) <= 25:
                return chalk.red.bold(progstr)
            if ( int( porcentram * 100 ) > 25 ) and ( int( porcentram * 100 ) <= 75 ):
                return chalk.yellow.bold(progstr)
            if int( porcentram * 100 ) > 75:
                return chalk.green.bold(progstr)
        
    def procentUse(porcent: float) -> str:
        porstr = str( int( porcent * 100)  ) + f"%" #porcentage with no decimals
        if int(porcent * 100) < 10:
            porstr = "  " + porstr
        if ( int(porcent * 100) >= 10 ) and ( int(porcent) < 100 ):
            porstr = " " + porstr
        return porstr

    useram = "[ " + ramd[0] + " |" + progressBar(progress) + "| " + procentUse(porcentram) + " - " + ramd[1] + "/" + ramd[3] + " " + ramd[4] +" ]"

    return useram


def printGeneralInfo(url1, local_filter):

    ## Filtered data from HCP
    file1 = open(url1 + local_filter, 'r')
    Lines = file1.readlines()
    
    #Generates lines without spaces and only usefull data
    for line in Lines:
        reg = re.sub(r'-\Dtype_[a-d]\D-\Dдоступно', "|", line)
        regf = re.sub(r'(-ядер:\D{2,3})|(:\D{1,2})|(\Dиз\D{2})|(\Dиз\D)', " ", reg)
        splitby = regf.split("|")
        print( chalk.bold( getNode(splitby[0]) + " --> " + getCPU(splitby[1]) + " " + getGPU(splitby[2]) + getRAM(splitby[3]) ) )


def getAvailableNode(url1, local_filter, ntasks, ngpus):

    ## Filtered data from HCP
    file1 = open(url1 + local_filter, 'r')
    Lines = file1.readlines()
    
    found = False
    fnode = ""

    #Generates lines without spaces and only usefull data
    for line in Lines:
        reg = re.sub(r'-\Dtype_[a-d]\D-\Dдоступно', "|", line)
        regf = re.sub(r'(-ядер:\D{2,3})|(:\D{1,2})|(\Dиз\D{2})|(\Dиз\D)', " ", reg)
        splitby = regf.split("|")
        iter_ntasks = splitby[1].lstrip().rstrip().split(" ")
        iter_gpus = splitby[2].lstrip().rstrip().split(" ")

        if not found:
            if not (iter_gpus[1] == "ет") :
                if ( int(iter_ntasks[1]) >= int(ntasks) ) and ( int(iter_gpus[1]) >= int(ngpus) ):
                    fnode = splitby[0].lstrip().rstrip()
                    found = True
            else:
                if not ( int(ngpus) > 0):
                    if int(iter_ntasks[1]) >= int(ntasks):
                        fnode = splitby[0].lstrip().rstrip()
                        found = True

    
    if found:
        print( chalk.bold( f"\nAvailable Node" ), f"........", f"[", chalk.green.bold(fnode), chalk.bold(f"]") )
        return fnode
    else:
        print( chalk.bold( f"\nAvailable Node" ), f"........", f"[", chalk.red.bold(f"Resources unavailable"), chalk.bold(f"]") )
        return "unavailable"
