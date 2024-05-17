#!/bin/sh

#SBATCH --account=proj_1460
#SBATCH --job-name=test
#SBATCH --constraint=type_b
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --nodelist=cn-[019]
#SBATCH --output=output-%j.log
#SBATCH --error=error-%j.err
#SBATCH --time=00:10:00

module purge
module load openmpi/4.1.4
module load CUDA/11.7
module load lammps/2022jun23_update1
srun --mpi=pmix_v2 lmp -i in.lj