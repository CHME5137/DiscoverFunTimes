#!/bin/sh
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --job-name=SA
#SBATCH --array=0-999%16
#SBATCH -e output_%a.log
#SBATCH -o output_%a.log
#SBATCH -p ser-par-10g

stdbuf -o0 -e0 python3 -u script.py
