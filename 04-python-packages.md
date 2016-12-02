# Adding Python packages

Because we're not using Ananconda on Discovery, but the
python3 installed by the system administrator, installing
additional Python packages is a little different from the
`conda install <package>` that we're used to.

> Notation: lines beginning `$ ` you should enter at a bash prompt,
(without entering an additional `$`). Lines beginning '>>> ' you should
enter at the python prompt (without entering an additional '>>> '),
and lines beginning `In [1]: ` you should enter at an ipython prompt
(you get the idea).
Other lines are just to show you what output you can expect.
Always see what output *you* actually get.

<br/>
> Important note: Following these instructions will have you run a few minimal Python things on the head login node, just to see if things work. Do *not* get carried away and do any real Python computations on the login nodes, as you will make Discovery slower for everyone else, get in trouble, and embarrass me (your account sponsor) for letting you break the terms of use! Learn how to use the compute nodes, in a later tutorial, before running any serious Python calculations!


First, load python3 and see which of our favorite libraries
are already installed.


```python
$ python3
Python 3.5.2 (default, Sep 19 2016, 11:10:34)
[GCC 4.4.6 20110731 (Red Hat 4.4.6-3)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy
>>> import scipy
>>> import scipy.integrate
>>> import matplotlib
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named 'matplotlib'
>>> import SALib
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named 'SALib'
```

So it looks like `numpy` and `scipy` are both installed, but `matplotlib` and `SALib` are not.
To see where the `numpy` came from:

```python
>>> numpy
<module 'numpy' from '/shared/apps/python/Python-3.5.2/Python-3.5.2/INSTALL/lib/python3.5/site-packages/numpy/__init__.py'>
```

It's in the centrally managed folder maintained by research-computing.
When you're done and want to leave the python3 terminal, type `exit()`
or press `Ctrl-D`.

A useful program for installing (and uninstalling) python packages is called `pip`.
A bit like `conda`, it figures out what the dependencies are and gets those too.
Let's see if we have it:

    $ which pip
    /shared/apps/python/Python-3.5.2/Python-3.5.2/INSTALL/bin/pip
    $ pip help

Looks good. Let's try using it to install `matplotlib`:

    $ pip install matplotlib

It will look promising, finding and downloading `matplotlib` and a few dependencies, but then when it tries to install it will give you an error. Ignore the warning about using an out of date version of pip,
the real problem is the line `PermissionError: [Errno 13] Permission denied: '/shared/apps/python/Python-3.5.2/Python-3.5.2/INSTALL/lib/python3.5/site-packages/...`
That's because we don't have [permission](http://www.ee.surrey.ac.uk/Teaching/Unix/unix5.html) to write to the centrally managed folder.
Fortunately, we can ask pip to install things in our own `$HOME` folder, where we
have write permissions:

    $ pip install --user matplotlib

Assuming that worked, go ahead and get SALib too:

    $ pip install --user SALib

And then test to see if it worked:

```python
$ python3
Python 3.5.2 (default, Sep 19 2016, 11:10:34)
[GCC 4.4.6 20110731 (Red Hat 4.4.6-3)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import matplotlib
>>> matplotlib
<module 'matplotlib' from '/home/r.west/.local/lib/python3.5/site-packages/matplotlib/__init__.py'>
>>> import SALib
>>> SALib
<module 'SALib' from '/home/r.west/.local/lib/python3.5/site-packages/SALib/__init__.py'>
>>> exit()
```

One other helpful package is called `ipython`. As well as python modules, this comes with some executables.
First check we don't have it:

    $ which ipython
    /usr/bin/which: no ipython in (/shared/apps/python/Python-3.5.2/Python-3.5.2/INSTALL/bin:/shared/apps/fftw/fftw-3.3.3/INSTALL/bin:/shared/apps/gnu-compilers/usr/bin:/usr/lib64/qt-3.3/bin:/opt/ibm/platform_mpi/bin:/shared/apps/lsf/9.1/linux2.6-glibc2.3-x86_64/etc:/shared/apps/lsf/9.1/linux2.6-glibc2.3-x86_64/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/home/r.west/bin)

It's not there, so let's try installing it.

    $ pip install --user ipython

There are many dependencies so it will install several other packages, but should succeed, and end with a message like `Successfully installed decorator-4.0.10 ipython-5.1.0 ipython-genutils-0.1.0 pexpect-4.2.1 pickleshare-0.7.4 prompt-toolkit-1.0.9 ptyprocess-0.5.1 pygments-2.1.3 simplegeneric-0.8.1 traitlets-4.3.1 wcwidth-0.1.7`.

Now let's try looking for the new `ipython` program:

    $ which ipython
    /usr/bin/which: no ipython in (/shared/apps/python/Python-3.5.2/Python-3.5.2/INSTALL/bin:/shared/apps/fftw/fftw-3.3.3/INSTALL/bin:/shared/apps/gnu-compilers/usr/bin:/usr/lib64/qt-3.3/bin:/opt/ibm/platform_mpi/bin:/shared/apps/lsf/9.1/linux2.6-glibc2.3-x86_64/etc:/shared/apps/lsf/9.1/linux2.6-glibc2.3-x86_64/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/home/r.west/bin)

Same result as before! We can't find it.
That's because `pip --user` installed it in the folder `~/.local/bin`, which isn't on our `$PATH`. If we add it to the end of our `$PATH` environment variable, it'll work:

    $ export PATH=$PATH:~/.local/bin
    $ which ipython
    ~/.local/bin/ipython
    $ ipython
    Python 3.5.2 (default, Sep 19 2016, 11:10:34)
    Type "copyright", "credits" or "license" for more information.

    IPython 5.1.0 -- An enhanced Interactive Python.
    ?         -> Introduction and overview of IPython's features.
    %quickref -> Quick reference.
    help      -> Python's own help system.
    object?   -> Details about 'object', use 'object??' for extra details.

    In [1]: import numpy

    In [2]: exit()

ipython is an interactive python shell, like we had when we ran `python3`,
but with some extra features like syntax highlighting, tab completion, and
on-the-spot help, like we got used to in Jupyter notebooks.
You can learn about them by typing `?` at
an ipython prompt, or reading https://ipython.org.

Remember: *don't* use it on the head login node (like we just did).

## Using matplotlib
We managed to install matplotlib, but can we use it?
*This section of tutorial should be moved to after we've learned to run interactive sessions on compute nodes, so we don't do it on the login node*.
First load `ipython` then try `from matplotlib import pyplot as plt` as we are used to doing.

```
$ ipython
Python 3.5.2 (default, Sep 19 2016, 11:10:34)
Type "copyright", "credits" or "license" for more information.

IPython 5.1.0 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]: from matplotlib import pyplot as plt
```

This will give a long error message, with the clue `# If this fails your Python may not be configured for Tk`.  Googling this will eventually lead you to try the following
, but I'll save you some time. You have to `exit()` your `ipython` session and start a new one (`$ ipython`):

 ```python
In [1]: import matplotlib

In [2]: matplotlib.use('Agg')

In [3]: from matplotlib import pyplot as plt
```

OK so far - no errors!  What we did is change the 'back end' that matplotlib uses, because Discovery is not set up with the default 'Tk', but does have 'Agg' ([don't ask me what these are](http://lmgtfy.com/?q=what+are+Tk+and+Agg)). You'll have to do this in any scripts that use matplotlib. Now let's try to make a plot.

```python
In [4]: plt.plot(range(5))
Out[4]: [<matplotlib.lines.Line2D at 0x7fc098b02a90>]
```

OK, but how do we see it?

```python
In [5]: plt.show()
```

Don't see anything? If you had installed an X11 window system and used X11 forwarding (`ssh -X`) then maybe you would have a local window appear. But when running a script on a remote computer it's usually more helpful to just save the figure to a file and retrieve it later:

```python
In [6]: plt.savefig("my_figure.pdf")

In [7]: exit()
```

Now look for the file:

```
$ ls *.pdf
my_figure.pdf
```

OK - it's there!  You can retrieve it using some SCP or SFTP commands, or preferably a client with a nice GUI (my favorite is currently [Forklift](http://www.binarynights.com/forklift/) but there are many good free ones to choose from).
