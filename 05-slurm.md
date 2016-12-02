# Submitting Slurm Jobs

First things first, we need to load [Slurm](https://slurm.schedmd.com/overview.html). The Slurm workload manager is a open-source job scheduler, that is currently being used on Discovery. Slurm does all the administration work of telling which jobs to run on which nodes, based on the conditions you give it. This allows multiple people to have access to the same computing resources.
To use it we need the slurm module:

	$ module load slurm-14.11.8

Refer back to [chapter 2](02-modules.md) for how to find the required dependencies and add
the necessarry `module load` commands to your `.bashrc` file.

Detailed instructions for this version of Slurm are [here](https://slurm.schedmd.com/archive/slurm-14.11.11/) should you need them, and the Discovery instructions are [here](http://nuweb12.neu.edu/rc/?page_id=18).

Let's assume that we have a python script, called `my_awesome_script.py` that we want to run. If we want to have slurm manage the job for us, we need to create a submission script, commonly titled `submit.sh`.

Here are some common headers for a `submit.sh` file:

	#!/bin/sh

The first line of a script beginning with `#!` tells the computer
how to interpret the script. In this case it's a shell script,
that will be run with the `sh` shell that can be found at `/bin` directory.

Then follows a number of lines beginning with `#SBATCH`, which tell Slurm how you want the job to be run.

	#SBATCH -n 1
	#SBATCH -N 1
	#SBATCH --job-name=hello
	#SBATCH -e error.log
	#SBATCH -o output.log
	#SBATCH -p ser-par-10g

These mean:
 * `-n` tells Slurm how many processors to run the job with. Your `my_awesome_script.py` file needs to be designed to take advantage of multiple processors to reap any benefits from having this greater than one.
 * `-N 1` will tell it to not split up the processors across multiple nodes. This can sometimes cause issues so it's usually safest to leave it in there.
 * `--job-name` tells slurm what to title your job, making it easier for you to find within all of the other running jobs.
 * `-e` and `-o` are where your standard error and standard output, respectively,  will be written to. These files will be over-written by other jobs (this can sometimes cause issues with running a job array - but that's for later). You can also point `-e` and `-o` to the same file, and both the errors and outputs will be written to the same file.
 * `-p` command tells slurm the *partition* that you would like to run the job on. More on those later.

There are many more options in [the sbatch manual](https://slurm.schedmd.com/archive/slurm-14.11.11/sbatch.html).

After the headers, you will need to add a line(s) (using system shell commands) to run your job.

	python3 my_awesome_script.py

to simply run the job, or

	stdbuf -o0 -e0 python3 -u my_awesome_script.py

if you have concerns about Slurm's buffer. (Sometimes the output from your script is buffered and does not appear in the output log file immediately. This is usually a good thing, making the file system access more efficient, but if your job crashes in certain ways before the buffer is flushed to disk, you may never see this output, making it harder to debug. These commands prevent buffering, and have helped us on occasion.)

Your `submit.sh` file should look something like this:

	#!/bin/sh
	#SBATCH -n 1
	#SBATCH --job-name=hello
	#SBATCH -e error.log
	#SBATCH -o output.log
	#SBATCH -p ser-par-10g

	stdbuf -o0 -e0 python -u my_awesome_script.py

You can then run the following command in your terminal window to submit the script:

	$ sbatch submit.sh

The following response should occur:

	Submitted batch job <job_number>

If you want to check the status of your job(s):

	$ squeue

Will show you the jobs of everything submitted to Discovery.

	$ squeue -u <user_name>

Will show you the jobs that you have submitted (eg. `squeue -u husky.id`).

	$ squeue -p <partition_name>

Will show you all the jobs on the partition you specify.

	$ scancel <job_number>

Will stop the job that you need to stop.

## Partitions

Some notes on choosing a partition...
Full details are [here](http://nuweb12.neu.edu/rc/?page_id=14)


---
Next: 6. [Running an interactive job.](06-interactive.md)
