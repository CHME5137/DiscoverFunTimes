# Anaconda (2019 version)

## First use
Setting up your anaconda environment.
Connect to discovery using SSH or the [OOD web console](10-ood.md)).

Type these at the terminal:
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
(for instructions on how to do so, see [chapter 3](03-bashrc.md) and [chapter 10](10-ood.md))

## Subsequent uses

Go to https://ood.discovery.neu.edu/ and log in. Request a job for no more than 1 hour.

