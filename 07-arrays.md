Okay, now we want to try and run a bunch of jobs at the same time. This is one way that we can parallelize jobs in Python, and is most useful in cases where jobs don't need to communicate with each other.

To get started, we need to add one more line to our `submit.sh` script.

	#SBATCH --array=1-1000%10
	#SBATCH -n 1

This example command will tell Slurm to run 1000 jobs, no more than 10 at a time.
(The `%10` part is optional).
Based on `-n`, each job will run on one processor.

Each job will have a number, 1 through 1000. Each number is accessible through both your job, and by SLURM. Here are a couple examples how it can be used:

If I want my python script to be able to access the number, this line will return the number.

```python
>>> os.getenv('SLURM_ARRAY_TASK_ID')
```

For example, in a script you might have something like:

```python
import os
job_number = int(os.getenv('SLURM_ARRAY_TASK_ID', default='0'))
parameters = big_paramater_list[job_number]
```

Because Python counts from zero, it may make sense to number your Slurm
array that way too, eg:

		#SBATCH --array=0-999


We discussed earlier how jobs will overwrite the output of the files that are specified in the submit script. If we are running an array of jobs,
we can add `%a` to the filenames in the `submit.sh` header to prevent two parallel jobs from having the same output/error file names.

	#SBATCH -o output_%a.log
	#SBATCH -e error_%a.log

## Try it out!

Clone this repository to your local computer, then look at [the Jupyter notebook](SAlib_example/SensitivityAnalysis.ipynb) in the `SAlib_example` folder to work through an example using an array job on Discovery to do a sensitivity analysis.

## Diagnosing problems

 * The maximum job array size on Discovery is 1001


Sometimes a job will have a problem, occasionally for no obvious reason,
and Slurm will requeue it in a held state. If there was no good reason,
eg. it was just assigned a node that was malfunctioning, or too busy,
it might be worth just trying the job again, which you can do with:

		$ scontrol release <jobid>

To see the status of your jobs, remember it's `squeue -u <username>`. For example:

		$ squeue -u r.west
				 JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
		 696611_33 ser-par-1       SA   r.west PD       0:00      1 (job requeued in held state)
		 696611_34 ser-par-1       SA   r.west PD       0:00      1 (job requeued in held state)
		 696611_35 ser-par-1       SA   r.west PD       0:00      1 (job requeued in held state)
		 696611_36 ser-par-1       SA   r.west PD       0:00      1 (job requeued in held state)
		 696611_37 ser-par-1       SA   r.west PD       0:00      1 (job requeued in held state)

This shows several of my jobs are requeued (in fact 48 of them - I showed the top 5).
I can release the first like this:

    $ scontrol release 696611_33

Now the queue shows `(None)` as the reason for it to be held...

		$ squeue -u r.west
				 JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
		 696611_33 ser-par-1       SA   r.west PD       0:00      1 (None)
		 696611_34 ser-par-1       SA   r.west PD       0:00      1 (job requeued in held state)
		 696611_35 ser-par-1       SA   r.west PD       0:00      1 (job requeued in held state)
		 696611_36 ser-par-1       SA   r.west PD       0:00      1 (job requeued in held state)
		 696611_37 ser-par-1       SA   r.west PD       0:00      1 (job requeued in held state)

...and the job will run on the next schedule (I think Discovery starts jobs every 30 seconds).

The benefit of having used an array job is we can release all of the held sub-jobs
with one command:

		$ scontrol release 696611

where the number is that of the parent job id (the bit before the underscore).

Otherwise, to release all of your held jobs you would need to do them one by one,
or piece together script-like command using your [command line fu](https://xkcd.com/196/):

		$ squeue -u r.west |  grep 'in held state' | awk '{print "scontrol release " $1}' | sh

If they get requeued again, perhaps something is wrong with your job and it's your fault, not Discovery's. Check the error and output logs for clues.
You can also type `scontrol show jobs <jobid>` to find out more about the
computer that it ran on, etc.
