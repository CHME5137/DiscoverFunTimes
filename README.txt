# type in source README.txt to make .bashrc, or if so inclined, try it
# yourself
#
# a Bash RC is used so you do not need to install modules into your user -
# (i.e. don't install anaconda) 
# The different modules have different dependencies that will need to be
# loaded before others can be loaded
#
# To find the dependencies, use the commands: module whatis <module name>
# for example: module load python-3.5.5
#
# You want to load, at the very least, python-3.5.2, and slurm-14.11.8
#
# If you give up, do this:
#

cp sample_bashrc.txt ~/.bashrc
source ~/.bashrc

