# Editing your .bashrc file

If there are some things you wish to do every time you log in to
the computer, such as load your required modules, configure
your terminal, or set some environment variables, then it
saves time to put them in a file that the `bash` shell will
run every time it starts. This is your `.bashrc` file, in your home
directory. It probably exists already (with some default contents)
but doesn't show up when you type `ls` because its name begins with
a `.` so it is hidden. To look for it, try:

    $ cd ~
    $ ls -al

To print its contents:

    $ cat .bashrc

To edit it, using the `vi` ext editor [(some instructions here)](https://www.cs.colostate.edu/helpdocs/vi.html):

    $ vi .bashrc

You want to add these commands, for `python3`:

    module load gnu-4.4-compilers
    module load fftw-3.3.3
    module load platform-mpi
    module load python-3.5.2

So that your `.bashrc` file looks something like:

```bash
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

module load gnu-4.4-compilers
module load fftw-3.3.3
module load platform-mpi
module load python-3.5.2
```

---
Next: 4. Installing additional Python modules
