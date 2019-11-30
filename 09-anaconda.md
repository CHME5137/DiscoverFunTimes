# Anaconda (2019 version)

First use, setting up your anaconda environment.
```
module load anaconda3/3.7
conda create -n myenv
source activate myenv
conda config --add channels conda-forge
conda install SALib
conda install -c cantera cantera
```


Put these lines in your `~/.bashrc` file:
```
module load anaconda3/3.7
source activate myenv
```
(for instructions on how to do so, see [chapter 3](03-bashrc.md))


Go to https://ood.discovery.neu.edu/ and log in. Request a job for no more than 1 hour.

