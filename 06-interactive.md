Okay, let us say we want to use a node interactively:


If you want to take advantage of Discovery while also using a graphical software (such as `GaussView`), you need to start by logging in with X11 forwarding:

	$ ssh -X surname.f@discovery2.neu.edu

You can find more details about loading X11 [here](01-logging-in.md).

We do not want to do anything resource intensive on the log in nodes (discovery2 and discovery4) as this will cause everyone difficulties, and ruffle some jimmies.

We need to request a compute node.

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

	[<username>@compute-0-006 ~]$

For example, if I want to run `GaussView` (and have all the proper modules installed):

	$ gview

(This is where you would find out that you need to use -Y instead of -X, but practice makes perfect!)

This is where you would do interactive python work eg. in ipython
(see [chapter 4](04-python-packages.md)).

Once you are done with your interactive session, log out of the compute node
by typing `exit` and then release the allocation using `scancel <jobID>`, e.g.:

```
r.west@compute-0-006 ~]$ exit
logout
Connection to compute-0-006 closed.
[r.west@discovery2 ~]$ scancel 649056
salloc: Job allocation 649056 has been revoked.
Hangup
[r.west@discovery2 ~]$
```

---
Next: 7. Submitting an array of jobs.
