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

But you could also edit it using the OOD web interface [described here](10-ood.md)

You want to add these commands, for Anaconda's Python 3:

    module load anaconda3/3.7

So that your `.bashrc` file looks something like:

```bash
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

module load anaconda3/3.7
```

**Remember!** Your `.bashrc` is only executed when you first log in to a computer,
so to test the effect of editing your `.bashrc` file you must log out and log
back in again.   (You can type `source .bashrc` to load an updated file, but
this will do it *on top of* the original file, and the effect may be unexpected.
It is safest to always log out and in again.)

Log out like this:

    $ logout

---
Next: [4. Installing additional Python packages](04b-python-packages.md)
