# Submitting Slurm Jobs

First things first, we need to load SLURM. The slurm workload manager is a open-source job scheduler, that is currently being used on Discovery. Slurm does all the admininstration work of telling which jobs to run on which nodes, based on the conditions you give it. This allows multiple people to have access to the same computing resources. So we need the slurm module: 
	
	module load slurm-14.11.8

Refer back to 02 - Loading modules if you forgot how to find the dependencies.

Let's assume that we have a job, called `input.py` that we want to run. If we want to have slurm manage the job for us, we need to create a submit file, commonly titled `submit.sh`.

Here are some common headers for a `submit.sh` file:

	#!/bin/sh

`#!/bin/sh` will point slurm to the system shell, where your linux comannds come from.

	#SBATCH -n 1

`#SBATCH` will tell slurm that you are telling it, specifically, how you want the job to be run. `-n` tells slurm how many processors to run the job with. Your `input.py` file needs to optimized to take advantage of multiple processors to reap any benefits.

	#SBATCH -N 1
	#SBATCH --job-name=hello
	#SBATCH -e error.log
	#SBATCH -o output.log
	#SBATCH -p ser-par-10g

`-N 1` will tell it to not split up the processors across multiple nodes. This can sometimes cause issues so it's usually safest to leave it in there. `--job-name` tells slurm what to title your job, making it easier for you to find within all of the other running jobs. `-e` and `-o` are where your standard error and standard output, respectively,  will be written to. These files will be over-written by other jobs (this can sometimes cause issues with running a job array - but that's for later). You can also point `-e` and `-o` to the same file, and both the errors and outputs will be written to the same file. The `-p` command tells slurm the node you would like to run the job on.

After the headers, you will need to add a line (using system shell commands) to run your job. 

	python your_script.py

to simply run the job or

	stdbuf -o0 -e0 python -u your_script.py

if you have concerns about slurm's buffer. 

Your `submit.sh` file should look something like this:

	#!/bin/sh
	#SBATCH -n 1
	#SBATCH --job-name=hello
	#SBATCH -e error.log
	#SBATCH -o output.log
	#SBATCH -p ser-par-10g

	stdbuf -o0 -e0 python -u your_script.py

You can then run the following command in your terminal window:

	$ sbatch submit.sh

The following response should occur:
	
	Submitted batch job <job_number>

If you want to double check on your job:

	$ squeue 

Will show you the jobs of everything submitted to Discovery. 

	$ squeue -u <user_name> 

Will show you the jobs that you have submitted.

	$ squeue -p <nodes_name> 

Will show you all the jobs on the collections of nodes you specify.

	$ scancel <job_number> 

Will stop the jobs that you need to stop.



