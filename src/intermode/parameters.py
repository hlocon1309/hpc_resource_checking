import os
from simple_chalk import chalk


def addToFile(text, mode):

    try:
        
        current_dirs_parent = os.path.dirname(os.getcwd())

        with open(current_dirs_parent + "/simulation/params.in", mode) as f:
            f.write(text)

    except IOError:
        print("Error: could not create file")


def parseUnits(param, uns):

    line = ""
    if param == "units":
        line += "units\t"
        units = ["lj", "real", "metal", "si", "cgs", "electron", "micro", "nano"]
        if uns in units:
            line += uns
            line += "\n"
            addToFile(line, 'w')
        else:
            print(chalk.red.bold(f'Unknown option for units'))


def parseBoundary(param, uns):

    line = ""
    if param == "boundary":
        line += "boundary\t"
        bounds = ["p p p"]
        if uns in bounds:
            line += uns
            line += "\n"
            addToFile(line, 'a')
        else:
            print(chalk.red.bold(f'Unknown option for boundary'))


def parseAtomStyle(param, ats):

    line = ""
    if param == "atom_style":
        line += "atom_style\t"
        atomStyle = ["angle", "atomic", "bond", "charge", "dipole", "full"]
        if ats in atomStyle:
            line += ats
            line += "\n"
            addToFile(line, 'a')
        else:
            print(chalk.red.bold(f'Unknown option for atom_style'))


def parseLattice(param, latt):

    line = ""
    if param == "lattice":
        line += "lattice\t"
        latticeStyle = ["bcc", "fcc", "hex", "sc"]
        pars = latt.split()
        if pars[0] in latticeStyle:
            line += pars[0]
        else:
            print(chalk.red.bold(f'Unknown option for lattice'))
        
        try:
            float(pars[1])
            varLattice = "\nvariable\tlatt\tequal "
            varLattice += pars[1]
            varLattice += "\n\n"
            line += "\t"
            line += "${latt}"
            line += "\n"
            varLattice += line
            addToFile(varLattice, 'a')
        except ValueError:
            # Handle the exception
            print(chalk.red.bold(f'Scale parameter is not a valid number'))


def parseRegionSolid(param, regSolid):

    line = ""
    line_f = ""
    var_par = ""
    if param == "region":
        line += "region\t"
        regionStyle = ["block"]
        pars = regSolid.split()
        if pars[1] in regionStyle:
            line += pars[0]
            line += " "
            line += pars[1]
        else:
            print(chalk.red.bold(f'Unknown option for region'))
        
        try:
            float(pars[2])
            float(pars[3])
            float(pars[4])
            float(pars[5])
            float(pars[6])
            float(pars[7])
            var_par += "\nvariable\tlx\tequal\t"
            var_par += pars[3]
            var_par += "\n"
            var_par += "variable\tly\tequal\t"
            var_par += "${lx}"
            var_par += "\n"
            var_par += "variable\tlz\tequal\t"
            var_par += "2*${lx}"
            var_par += "\n\n"
            line_f += var_par
            line_f += line
            line_f += " "
            line_f += pars[2]
            line_f += " "
            line_f += "${lx} "
            line_f += pars[4]
            line_f += " "
            line_f += "${ly} "
            line_f += pars[6]
            line_f += " "
            line_f += "${lz}"
            line_f += "\n"
            addToFile(line_f, 'a')

        except ValueError:

            print(chalk.red.bold(f'Some Args parameters are not a valid number'))


def parseCreateBox(param, uns):
    line = ""
    if param == "create_box":
        line += "create_box "
        if uns == "1 box":
            line += uns
            line += "\n"
            addToFile(line, 'a')
        else:
            print(chalk.red.bold(f'Unknown option'))


def parseCreateAtoms(param, uns):
    line = ""
    if param == "create_atoms":
        line += "create_atoms "
        if uns == "1 box":
            line += uns
            line += "\n"
            addToFile(line, 'a')
        else:
            print(chalk.red.bold(f'Unknown option'))


def parseMass(param, uns):
    line = ""
    if param == "mass":
        line += "mass "
        if uns == "1 1.0":
            line += uns
            line += "\n"
            addToFile(line, 'a')
        else:
            print(chalk.red.bold(f'Unknown option'))


def parseVelocity(param, uns):
    line = ""
    if param == "velocity":
        line += "velocity "
        if uns == "all create 1.0 87287 dist gaussian":
            line += uns
            line += "\n"
            addToFile(line, 'a')
        else:
            print(chalk.red.bold(f'Unknown option'))


def parsePairStyle(param, uns):
    line = ""
    if param == "pair_style":
        line += "pair_style "
        if uns == "lj/cut 2.5":
            line += uns
            line += "\n"
            addToFile(line, 'a')
        else:
            print(chalk.red.bold(f'Unknown option'))


def parsePairCoeff(param, uns):
    line = ""
    if param == "pair_coeff":
        line += "pair_coeff "
        if uns == "1 1 1.0 1.0 2.5":
            line += uns
            line += "\n"
            addToFile(line, 'a')
        else:
            print(chalk.red.bold(f'Unknown option'))


def parsePairModify(param, uns):
    line = ""
    if param == "pair_modify":
        line += "pair_modify "
        if uns == "tail yes":
            line += uns
            line += "\n"
            addToFile(line, 'a')
        else:
            print(chalk.red.bold(f'Unknown option'))


def parseNeighbor(param, uns):
    line = ""
    if param == "neighbor":
        line += "neighbor "
        if uns == "0.3 bin":
            line += uns
            line += "\n"
            addToFile(line, 'a')
        else:
            print(chalk.red.bold(f'Unknown option'))


def parseThermoStyle(param, uns):
    line = ""
    if param == "thermo_style":
        line += "thermo_style "
        if uns == "custom step pe ke etotal temp press density":
            line += uns
            line += "\n"
            addToFile(line, 'a')
        else:
            print(chalk.red.bold(f'Unknown option'))


def parseThermo(param, uns):
    line = ""
    if param == "thermo":
        line += "thermo "
        if uns == "100":
            line += uns
            line += "\n"
            addToFile(line, 'a')
        else:
            print(chalk.red.bold(f'Unknown option'))


def parseThermoModify(param, uns):
    line = ""
    if param == "thermo_modify":
        line += "thermo_modify "
        if uns == "norm no":
            line += uns
            line += "\n"
            addToFile(line, 'a')
        else:
            print(chalk.red.bold(f'Unknown option'))


def parseFix(param, uns):
    line = ""
    if param == "fix":
        line += "fix "
        if uns == "1 all nve":
            line += uns
            line += "\n"
            addToFile(line, 'a')
        else:
            print(chalk.red.bold(f'Unknown option'))


def parseTimeStep(param, uns):
    line = ""
    if param == "timestep":
        line += "timestep "
        if uns == "0.005":
            line += uns
            line += "\n"
            addToFile(line, 'a')
        else:
            print(chalk.red.bold(f'Unknown option'))


def parseRun(param, uns):
    line = ""
    if param == "run":
        line += "run "
        if uns == "1000":
            line += uns
            line += "\n"
            addToFile(line, 'a')
        else:
            print(chalk.red.bold(f'Unknown option'))


def complements():

    line = ""
    print(chalk.yellow.bold(f'Generating complement parameters: '))

    print(chalk.yellow.bold(f'\t-> unfix\t1'))
    line += "unfix\t1\n"

    print(chalk.yellow.bold(f'\t-> fix\t2 all nvt temp 1.0 1.0 0.1'))
    line += "fix\t2 all nvt temp 1.0 1.0 0.1\n"

    print(chalk.yellow.bold(f'\t-> run\t1000'))
    line += "run\t1000\n\n"

    print(chalk.yellow.bold(f'\t-> dump\t1 all xyz 100 output.xyz'))
    line += "dump\t1 all xyz 100 output.xyz\n"

    print(chalk.yellow.bold(f'\t-> dump_modify\t1 element Ar'))
    line += "dump_modify\t1 element Ar\n"

    print(chalk.yellow.bold(f'\t-> run\t2000'))
    line += "run\t2000\n"
    
    addToFile(line, 'a')


def readParams():

    print(chalk.cyan.bold(f'>>> INTERACTIVE MODE <<<\n'))


    #units
    units = input(chalk.bold(f'Enter parameter for units: [lj] '))
    if units:
        parseUnits("units", units)
    else:
        parseUnits("units", "lj")
    

    #boundary
    bounds = input(chalk.bold(f'Enter parameter for boundary: [p p p] '))
    if bounds:
        parseBoundary("boundary", bounds)
    else:
        parseBoundary("boundary", "p p p")
    

    #atom_style
    atom_style = input(chalk.bold(f'Enter parameter for atom_style: [full] '))
    if atom_style:
        parseAtomStyle("atom_style", atom_style)
    else:
        parseAtomStyle("atom_style", "full")
    

    #lattice
    lattice = input(chalk.bold(f'Enter parameter for lattice: [sc 0.5] '))
    if lattice:
        parseLattice("lattice", lattice)
    else:
        parseLattice("lattice", "sc 0.5")


    #region_
    region = input(chalk.bold(f'Enter parameter for solid region: [box block 0 10 0 10 0 10] '))
    if region:
        parseRegionSolid("region", region)
    else:
        parseRegionSolid("region", "box block 0 10 0 10 0 10")


    #create_box
    create_box = input(chalk.bold(f'Enter parameter for create_box: [1 box] '))
    if create_box:
        parseCreateBox("create_box", create_box)
    else:
        parseCreateBox("create_box", "1 box")
    

    #create_atoms
    create_atoms = input(chalk.bold(f'Enter parameter for create_atoms: [1 box] '))
    if create_atoms:
        parseCreateAtomst("create_atoms", create_atoms)
    else:
        parseCreateAtoms("create_atoms", "1 box")
    

    #mass
    mass = input(chalk.bold(f'Enter parameter for mass: [1 1.0] '))
    if mass:
        parseMass("mass", mass)
    else:
        parseMass("mass", "1 1.0")
    
    
    #velocity
    velocity = input(chalk.bold(f'Enter parameter for velocity: [all create 1.0 87287 dist gaussian] '))
    if velocity:
        parseVelocity("velocity", velocity)
    else:
        parseVelocity("velocity", "all create 1.0 87287 dist gaussian")
    
    
    #pair_style
    pair_style = input(chalk.bold(f'Enter parameter for pair_style: [lj/cut 2.5] '))
    if pair_style:
        parsePairStyle("pair_style", pair_style)
    else:
        parsePairStyle("pair_style", "lj/cut 2.5")


    #pair_coeff
    pair_coeff = input(chalk.bold(f'Enter parameter for pair_coeff: [1 1 1.0 1.0 2.5] '))
    if pair_coeff:
        parsePairCoeff("pair_coeff", pair_coeff)
    else:
        parsePairCoeff("pair_coeff", "1 1 1.0 1.0 2.5")


    #pair_modify
    pair_modify = input(chalk.bold(f'Enter parameter for pair_modify: [tail yes] '))
    if pair_modify:
        parsePairModify("pair_modify", pair_modify)
    else:
        parsePairModify("pair_modify", "tail yes")


    #neighbor
    neighbor = input(chalk.bold(f'Enter parameter for neighbor: [0.3 bin] '))
    if neighbor:
        parseNeighbor("neighbor", neighbor)
    else:
        parseNeighbor("neighbor", "0.3 bin")


    #thermo_style
    thermo_style = input(chalk.bold(f'Enter parameter for thermo_style: [custom step pe ke etotal temp press density] '))
    if thermo_style:
        parseThermoStyle("thermo_style", thermo_style)
    else:
        parseThermoStyle("thermo_style", "custom step pe ke etotal temp press density")


    #thermo
    thermo = input(chalk.bold(f'Enter parameter for thermo: [100] '))
    if thermo:
        parseThermo("thermo", thermo)
    else:
        parseThermo("thermo", "100")
    

    #thermo_modify
    thermo_modify = input(chalk.bold(f'Enter parameter for thermo_modify: [norm no] '))
    if thermo_modify:
        parseThermoModify("thermo_modify", thermo_modify)
    else:
        parseThermoModify("thermo_modify", "norm no")


    #fix
    fix = input(chalk.bold(f'Enter parameter for fix: [1 all nve] '))
    if fix:
        parseFix("fix", fix)
    else:
        parseFix("fix", "1 all nve")
    

    #timestep
    timestep = input(chalk.bold(f'Enter parameter for timestep: [0.005] '))
    if timestep:
        parseTimeStep("timestep", timestep)
    else:
        parseTimeStep("timestep", "0.005")


    #run
    run = input(chalk.bold(f'Enter parameter for run: [1000] '))
    if run:
        parseRun("run", run)
    else:
        parseRun("run", "1000")


    #writing other params
    complements()
    
