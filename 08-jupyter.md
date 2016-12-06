# Running Jupyter Notebooks on Discovery

First, check if jupyter is installed

    $ which jupyter
      /usr/bin/which: no jupyter in (/opt/ibm/platform_mpi/bin:/shared/apps/lsf/9.1/linux2.6-glibc2.3-x86_64/etc:/shared/apps/lsf/9.1/linux2.6-glibc2.3-x86_64/bin:/shared/apps/python/Python-3.5.2/Python-3.5.2/INSTALL/bin:/shared/apps/slurm/slurm-14.11.8/INSTALL/sbin:/shared/apps/slurm/slurm-14.11.8/INSTALL/bin:/shared/apps/perl/perl-5.20.0/INSTALL/bin:/shared/apps/fftw/fftw-3.3.3/INSTALL/bin:/shared/apps/gnu-compilers/usr/bin:/usr/lib64/qt-3.3/bin:/opt/ibm/platform_mpi/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/home/r.west/.local/bin:/home/r.west/bin:/home/r.west/.local/bin)

Now use pip to install it in your $HOME userspace:

    $ which pip
    /shared/apps/python/Python-3.5.2/Python-3.5.2/INSTALL/bin/pip
    $ pip install --user jupyter

And check you can find it (you should have put `.local/bin` at the end of your `$PATH` in your `.bashrc` file during [chapter 4](04-python-packages.md))

    $ which jupyter
    ~/.local/bin/jupyter

Now, request allocation for an interactive job, as we learned in [chapter 6](06-interactive.md):
First check which partitions have some idle nodes using `sinfo`, then request allocation on one using `salloc`, wait a moment, then find out which node you were given using `squeue`, then `ssh` to it.

    $ sinfo | grep idle
    $ salloc -N 1  --exclusive -p ht-10g-4
    $ squeue -u r.west
    $ ssh -X compute-3-041
    Last login: Tue Dec  6 08:46:01 2016 from discovery2

Then try running `jupyter notebook` and read the output carefully.

    [r.west@compute-3-041 ~]$ jupyter notebook
    [I 08:54:25.409 NotebookApp] Serving notebooks from local directory: /home/r.west
    [I 08:54:25.409 NotebookApp] 0 active kernels
    [I 08:54:25.409 NotebookApp] The Jupyter Notebook is running at: http://localhost:8888/
    [I 08:54:25.409 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
    [W 08:54:25.412 NotebookApp] No web browser found: could not locate runnable browser.


Jupyter runs a mini webserver which you access through your web browser.
It normally opens this browser for you, pointing to the correct URL, so
you don't usually need to worry about how it works.
The last line in the output above is telling you that it couldn't find a web browser on the compute node.
One option would be to ask the system administrators to install one;
but they will look at you funny (the compute nodes can't access the web, and don't have a screen, so what would you browse and how?). But if there was a browser, you could `ssh` with the `-X` (or `-Y`) option, and hope the browser windows appear on your own screen. But it would be very laggy and annoying, especially if you weren't on a super-fast connection to [Holyoke](http://www.mghpcc.org/about/about-the-mghpcc/).

Better plan is to use our own web browser, and connect to Jupyter's web server. A few lines before that in the output, Jupyter tells you what the address is - importantly, which port it is serving on: `The Jupyter Notebook is running at: http://localhost:8888/`.
If port `8888` was busy when you started the notebook, it'll use `8889`, etc.  The trouble is, that port is only being served locally, from the compute node to itself! (hence the web address `localhost`). We can't connect to it from anywhere else.

The solution is to tunnel to it, through a new ssh connection.

> The following instructions are for a Mac, Linux, Windows using a bash shell, where you type `ssh` in a terminal to connect via ssh. If you are on Windows and using Putty for your ssh connections, the options for port forwarding are somewhere in the GUI menus. Read [this](https://howto.ccs.neu.edu/howto/windows/ssh-port-tunneling-with-putty/) or ask google if you can't figure it out, then update this tutorial with a few pointers!

Leaving the existing ssh connection running, open a new terminal window (or tab) on your local computer (eg. `New Tab` from the `Shell` menu on OS X), and use it to open a new ssh connection, this time with port forwarding:

    $ ssh -L 8888:compute-3-041:8888 r.west@discovery2.neu.edu

This new option requests that port 8888 on my local computer is forwarded (through the ssh tunnel to discovery2) to port 8888 on the remote computer compute-3-041.  You will have to change the compute node name, port number, and your username.
When I try this it logged in OK and looks like it worked, but read the first few lines of output carefully:

```
$ ssh -L 8888:compute-3-041:8888 r.west@discovery2.neu.edu
bind: Address already in use
channel_setup_fwd_listener_tcpip: cannot listen to port: 8888
Could not request local forwarding.
Last login: Tue Dec  6 08:34:10 2016 from c-65-96-167-0.hsd1.ma.comcast.net
+---------------------------------------------------------------------------+
| Northeastern University Research Computing Cluster (discovery.neu.edu)    |
| Login Node                                                                |
+---------------------------------------------------------------------------+
| Usage of this cluster assumes you have read and agree to usage guidelines |
| at http://www.northeastern.edu/rc.                                        |
|                                                                           |
| Please do not run interactive jobs or GUIs on this node, it is against    |
| usage policy that you agreed to when applying for the cluster account.    |
|                                                                           |
| See "Submitting Jobs on Discovery Cluster" page at                        |
| http://www.northeastern.edu/rc or contact researchcomputing@neu.edu.      |
|                                                                           |
| If you have reached this node in error please logout now and send an      |
| email with your login id to researchcomputing@neu.edu.                    |
|                                                                           |
| All other requests should be directed to researchcomputing@neu.edu.       |
|                                                                           |
| Thank you,                                                                |
| NU Research Computing Team (researchcomputing@neu.edu)                    |
+---------------------------------------------------------------------------+
[r.west@discovery2 ~]$
```

It "cannot listen to port: 8888" because it is "already in use". I already have a local jupyter notebook running on my local port 8888!
So I disconnect (`$ logout`) and try again, forwarding my local port 8912 (arbitrary choice probably not being used) to the remote port 8888:

    $ ssh -L 8912:compute-3-041:8888 r.west@discovery2.neu.edu

This time it connects without any warning or error lines.
However, any attempt to connect to the server in my browser fails, because it wants to serve on 8888 but is receiving requests from a browser expecting 8912.
So I close that connection too (`$ logout`) and open a new one connecting port 8912 to port 8912:

    $ ssh -L 8912:compute-3-041:8912 r.west@discovery2.neu.edu

Then I go back to the terminal window that was running `jupyter`, shut down the jupyter server by pressing Ctrl-C (`^C`) twice, then start it again on port 8912:

    $ jupyter notebook --port 8912

This still does not work because, for security reasons, jupyter is configured to only accept connections from `localhost` [(see here)](http://jupyter-notebook.readthedocs.io/en/latest/public_server.html) and not other computers.
I tried following the instructions to generate a configuration file and change this setting, but (a) it would make it less secure, and (b) I couldn't get it to work anyway.

My final approach, was to tunnel all the way through to the compute node using SSH, so the jupyter notebook thinks the connection *is* coming from itself (`localhost`).  Leave your notebook serving on port 8912, but in the other window disconnect your existing ssh tunnels (`$ logout`) and then connect first to discovery2 and then to the compute node, forwarding port 8912 to localhost each time:

    RichardsMacBookPro13:DiscoverFunTimes rwest$ ssh -L 8912:localhost:8912 r.west@discovery2.neu.edu
    [r.west@discovery2 ~]$ ssh -L 8912:localhost:8912 compute-3-041
    [r.west@compute-3-041 ~]$

Now open a web browser and point it to http://localhost:8912/ !

To test it works as well as we can hope:

```python
import matplotlib
matplotlib.use('Agg')
%matplotlib inline
from matplotlib import pyplot as plt

plt.plot(range(5))
```

When done, be sure to shut down and disconnect all your sessions (lazy way: press Ctrl-C and Ctrl-D a lot in each window!), to release the resources back to the Slurm queues.


## Why?

Why would it be helpful to run Jupyter on Discovery instead of on your own computer?
One example was the sensitivity analysis in chapter 7b: we had to copy files back and forth to the server a bunch, especially when debugging. If we did the analysis in a notebook on Discovery, the data would be right there!

Also helpful if you are analyzing very large data files - Discovery has many terabytes of fast storage available. (Although *not* in your default `$HOME` directory - so be sure to ask research-computing for help and advice if you have "big data" to deal with).

## Why not?

Remember: Although Jupyter Notebooks are a great way to try things out and do one-off bits of analysis, and good for presenting your results, as your simulations get more complicated you probably want to be writing Python scripts and modules, and using an IDE like PyCharm to help you. Develop your code locally, once it's running and debugged, upload to Discovery and run it as a script.  The other drawback of Jupyter Notebooks is collaboration with peers on git: it's *much* harder to merge simultaneous changes in a notebook than in a python script. 
