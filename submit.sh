#!/bin/sh
#SBATCH -n 20
#SBATCH -N 1
#SBATCH --job-name=rand
#SBATCH --array=1-1000%10
#SBATCH -e output_%a.log
#SBATCH -o output_%a.log
#SBATCH -p west

export GAUSS_SCRDIR="/gss_gpfs_scratch/cain.ja"

stdbuf -o0 -e0 python -u input.py
