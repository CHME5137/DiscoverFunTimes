#!/bin/sh
#SBATCH -n 1
#SBATCH --job-name=hello
#SBATCH -e error.log
#SBATCH -o output.log
#SBATCH -p ser-par-10g


stdbuf -o0 -e0 python -u your_script.py
