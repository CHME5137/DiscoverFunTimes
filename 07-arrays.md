Okay, now we want to try and run a bunch of jobs at the same time. This is one way that we can parallelize jobs in Python, and is most useful in cases where jobs don't need to communicate with each other.

To get started, we need to add one more line to our `submit.sh` script.

	#SBATCH --array=1-1000%10
	#SBATCH -n 1

This example command will tell Slurm to run 1000 jobs, 10 at a time. Based on `-n`, each job will run on one processor.

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


We discussed earlier how jobs will overwrite the output of the files that are specified in the submit script. If we are running an array of jobs,
we can add `%a` to the filenames in the `submit.sh` header to prevent two parallel jobs from having the same output/error file names.

	#SBATCH -o output_%a.log
	#SBATCH -e error_%a.log

Try it out!
