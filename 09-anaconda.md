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


Subsequent uses
```
module load anaconda3/3.7
source activate myenv
```

