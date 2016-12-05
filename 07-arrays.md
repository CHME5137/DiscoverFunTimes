Okay, now we want to try and run a bunch of jobs at the same time. This is one way that we can parallelize jobs in Python, and is most useful in cases where jobs don't need to communicate with each other.

To get started, we need to add one more line to our `submit.sh` script. 

	#SBATCH --array=1-1000%10
	#SBATCH -n 1	
 
This example command will tell SLURM to run 1000 jobs, 10 at a time. Based on `-n`, each job will run on one processor.

Each job will have a number, 1 through 1000. Each number is accessible through both your job, and by SLURM. Here are a couple exampbles how it can be used:

If I want my python script to be able to access the number, this line will return the number.

```python
>>> os.getenv('SLURM_ARRAY_TASK_ID')
```

We discussed earlier how jobs will overwrite the output of the files that are specified in the submit script. If we are running jobs, we can %a to the filenames in the `submit.sh` header to prevent two parallel jobs from having the same output/error file names. 

	#SBATCH -e output_%a.log

Try it out!


