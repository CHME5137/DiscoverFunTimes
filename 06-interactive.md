Okay, let us say we want to use a node interactively:

If you want to take advantage of Discovery while also using a graphical software (such as `GaussView`), you need to start by logging in with X11 forwarding:

	$ ssh -X surname.f@discovery2.neu.edu

You can find more details about loading X11 [here](01-logging-in.md).

Remember how we do not want to do anything resource intensive on the log in nodes (discovery2 and discovery4)?
Doing so would cause everyone difficulties, and ruffle some jimmies.
Requesting an interactive job and logging in to a compute node is the solution.

First we need to request a compute node to use.

	$ salloc -N 1  --exclusive -p ht-10g
	salloc: Granted job allocation 649056

This will request exclusive use of a free node on partition `ht-10g`.
(It would make sense to check the queues before choosing a partition, for example `sinfo | grep idle` will show how many idle nodes are in each partition.
	One of the `ser-par-10g-` partitions is usually a good bet.)

To find out which node you were allocated by Slurm:

	$ squeue -u <username>

where <username> is your username, eg. husky.id.
For example, it will look like this:

	         JOBID PARTITION     NAME        USER ST       TIME  NODES NODELIST(REASON)
	        649056    ht-10g     bash  <username>  R       0:08      1 compute-0-006

This tells us our job 649056 is running on node compute-0-006.
Then log in to your shiny new compute node!

	$ ssh -X compute-0-006

Sometimes, it may prompt you for a password. Just Ctrl-C and try to `ssh -X <compute-node>` again.

Now you're on an interactive session!

	[<user_name>@compute-0-006 ~]$

(This is where you would find out that you need to use -Y instead of -X, but practice makes perfect!)

Next: 7. [Submitting an array of jobs.](07-arrays.md)
