Okay, let us say we want to use a node interactively:


If you want to take advantage of Discovery while also using a graphical software (such as `GaussView`), We need to start with logging in with X11:

	$ ssh -X surname.f@discovery2.neu.edu

You can find more details about loading X11 [here](01-logging-in.md).

Remember how we do not want to do anything resource intensive on the log in nodes (discovery2 and discovery4)? This will cause everyone difficulties, and ruffle some jimmies. 
This is the solution.

We need to request a compute node.

	$ salloc -N 1  --exclusive -p ht-10g

This will request a free node on partition ht-10g.

To find out which node we were allocated by SLURM:

	$ squeue -u <user_name>

For example, it will look like this:


	             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
	            649056    ht-10g     bash <user-name>  R       0:08      1 compute-0-006

Then log in to your shiny new compute node!

	$ ssh -X compute-0-006

Sometimes, it may prompt you for a password. Just Ctrl-C and try to `ssh -X <compute-node>` again.

Now you're on an interactive session!
	
	[<user_name>@compute-0-006 ~]$ 

If I want to run `GaussView` (and have all the proper modules installed):
	
	$ gview

(This is where you would find out that you need to use -Y instead of -X, but practice makes perfect!)

Next: 7. [Submitting an array of jobs.](07-arrays.md)
