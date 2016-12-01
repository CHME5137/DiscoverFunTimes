# Loading modules

> *Notation: lines beginning with a `$` you should enter at the terminal, which typically ends with a `$` (but don't enter an additional `$`).*

The research computing staff maintain a lot of software on discovery,
but it is not all compatible with each other (there are different versions
  of the same software, for example) so it is not all available
all of the time by default - you have to choose which you want to load.
These are organized in modules.

List the available modules:

    $ module avail

As you can see, there are a lot, including quantum chemistry packages,
molecular dynamics packages, specialized compilers, matlab, etc.
See for example there are three versions of python:

    python-2.7.5
    python-3.3.2
    python-3.5.2

You probably want the last one, but find out more about it by typing:

    $ module whatis python-3.5.2

This will tell you about it, and crucially, a list of the prerequisites, in the correct order.
These contain compilers and libraries that the software you want was compiled against, and
are needed for it to run.
It suggests putting these module load commands in your `.bashrc` file, which we will get to
in the next tutorial. For now, we will just type them by hand.
But before you do that, let's see what python you will get without loading the modules.
There may be several programs called
`python` and when you type `python` the computer has to pick one of them to run.
The way it does this is by searching through all the directories listed in your `$PATH` until it finds one containing
an executable called `python`, and runs that.
I can see my current `$PATH` by typing `echo $PATH`:

    $ echo $PATH
    /usr/lib64/qt-3.3/bin:/opt/ibm/platform_mpi/bin:/shared/apps/lsf/9.1/linux2.6-glibc2.3-x86_64/etc:/shared/apps/lsf/9.1/linux2.6-glibc2.3-x86_64/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/home/r.west/bin

The `which` program is a helpful command that tells you which executable program will
be run when you ask for a given program. ie. which is the first directory in your `$PATH`
that contains an executable with the requested name. For example:

    $ which python
    /usr/bin/python

To see what version this is:

    $ python -V
    Python 2.6.6

Let's see if there's a `python3` program:

    $ which python3
    /usr/bin/which: no python3 in (/usr/lib64/qt-3.3/bin:/opt/ibm/platform_mpi/bin:/shared/apps/lsf/9.1/linux2.6-glibc2.3-x86_64/etc:/shared/apps/lsf/9.1/linux2.6-glibc2.3-x86_64/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/home/r.west/bin)

This is telling us that there is no executable called `python3` in any of the directories listed in the `$PATH`. If I were to try executing it, it would fail:

    $ python3
    -bash: python3: command not found

Now let's load the modules we found out about earlier:

    $ module load gnu-4.4-compilers
    $ module load fftw-3.3.3
    $ module load platform-mpi
    $ module load python-3.5.2

Or you could do them all in one go (but in the correct order):

    $ module load gnu-4.4-compilers fftw-3.3.3 platform-mpi python-3.5.2

And try again:

    $ which python
    /usr/bin/python

That is the same as before!:

    $ python -V
    Python 2.6.6

But now we have a new program called `python3` available, which wasn't before:

    $ which python3
    /shared/apps/python/Python-3.5.2/Python-3.5.2/INSTALL/bin/python3
    $ python3 -V
    Python 3.5.2

Now we can execute it, type some python commands, and get the results.
Press control-D to quit it when you're done:

    $ python3
    Python 3.5.2 (default, Sep 19 2016, 11:10:34)
    [GCC 4.4.6 20110731 (Red Hat 4.4.6-3)] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> print("Hello, World!")
    Hello, World!
    >>>


If you want some new software installed, it's often easiest to just ask the friendly folks at
researchcomputing@northeastern.edu to install it for you as a new module, than trying
to configure and compile it yourself.

When loading a new module remember to always use `module whatis` to find out what the
prerequisites are.  If you want to run several programs at the same time, and aren't sure
what order to load the combined list of prerequisites in, try a few sensible combinations
then ask researchcomputing@northeastern.edu for help!
