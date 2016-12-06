#!/bin/sh
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --job-name=SA
#SBATCH --array=0-99
#SBATCH -p ser-par-10g
#SBATCH -e error_%a.log
#SBATCH -o output_%a.log
stdbuf -o0 -e0 python3 -u script2.py
