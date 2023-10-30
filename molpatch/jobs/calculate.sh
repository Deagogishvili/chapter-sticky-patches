#!/bin/bash

#SBATCH --job-name=molpatch
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=3
#SBATCH --time=120:00:00
#SBATCH --error=process.err
#SBATCH --output=process.out

module load 2022
module load 2022 Xvfb/21.1.3-GCCcore-11.3.0
#module load 2023

source activate mp

echo "preparing"

cd ../ResidueBased
python3 calculate.py 

Echo "done"
