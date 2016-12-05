
# coding: utf-8

# # Using Sensitivity Analysis to Interrogate Models
# 
# Original notebook: Will Usher, UCL Energy Institute, 10th December 2015 <br/>
# Updates to demonstrate running array jobs on a cluster: Richard West, 2016
# 
# In this version, most of the background and detail have been removed. Please refer to the original at https://github.com/SALib/SATut if you are not familiar with the system.

# In[1]:

from ipywidgets import widgets, interact
from IPython.display import display
get_ipython().magic('matplotlib inline')
import seaborn as sbn
import matplotlib.pyplot as plt
import numpy as np
from IPython.core.pylabtools import figsize
figsize(12, 10)
sbn.set_context("talk", font_scale=1)

# The model used for this seminar is contained in the file model.py
from model import cost_of_vehicle_to_grid, compute_profit, annualized_capital_cost, battery_lifetime, max_vehicle_power


# In[2]:

# Uncomment and execute the following line to see the contents of the `model.py` file
# %load model.py


# ## Using SALib to run a Sensitivity Analysis
# 
# As we saw earlier, SALib is a **free** **open-source** **Python** library which you can install by running the command
# 
# ```python
# pip install SALib
# ```
# 
# [Documentation](http://salib.readthedocs.org/) is available online.
# 

# ### Import the package

# In[4]:

from SALib.sample import morris as ms
from SALib.analyze import morris as ma
from SALib.plotting import morris as mp


# ### Define a problem file
# 
# In the code below, a problem file is used to define the variables we wish to explore

# In[5]:

morris_problem = {
    # There are six variables
    'num_vars': 7,
    # These are their names
    'names': ['conn', 'batt', 'dist', 'range', 'dri_eff', 'inv_eff', 'dispatch_time'],
    # These are their plausible ranges over which we'll move the variables
    'bounds': [[2.3, 22], # connection_power (kW)
               [50, 100], # battery size (kWh)
               [0, 80], # distance driven (km)
               [0, 80], # range buffer (km)
               [4,5.5], # driving efficiency (kWh/km)
               [0.87,0.97], # inverter efficienct (%)
               [0.5, 24] # dispatch time - hours of the day in which the energy is dispatched
              ],
    # I don't want to group any of these variables together
    'groups': None
    }


# ### Generate a Sample
# 
# We then generate a sample using the `morris.sample()` procedure from the SALib package.

# In[6]:

number_of_trajectories = 1000
sample = ms.sample(morris_problem, number_of_trajectories, num_levels=4, grid_jump=2)
print("The sample array is ",sample.shape)
print("Here are the first 10 rows:")
for j in range(10):
    print(' '.join(['{:10.3f}'.format(i) for i in sample[j]]))


# Now we're going to save the parameters to a file, so we can run the jobs separately not in this notebook.

# In[7]:

np.savetxt("parameter_values.txt", sample)
with open("results.txt", 'w') as result_file:  # 'w' is write mode, and will clear the file.
    result_file.write('')


# # Stop!  
# ## Now (pretend) we need to run the simulations on Discovery
# 
# To run this on Discovery, you will need to copy the `parameter_values.txt` and `results.txt` files on to Discovery, along with a Python script file (eg. `my_script.py`) that looks like the following cell.  Use an SCP or SFTP program, as described earlier in the tutorial.

# In[8]:

# This is a script that you should run on Discovery, as part of a Slurm Array job.
# Don't just run this cell in the notebook.
import numpy as np
import os
from model import max_vehicle_power
big_parameter_list = np.loadtxt("parameter_values.txt")
job_number = int(os.getenv('SLURM_ARRAY_TASK_ID', default='0'))
parameters = big_parameter_list[job_number]
parameters
result = max_vehicle_power(*parameters)
"""
Because we don't know what order the jobs will complete in,
the results may be written out of order!
To deal with this, we will write the job number in the results file
as well as the result:
"""
with open("results.txt", 'a') as result_file: # 'a' is append mode, and will add to the file.
    result_file.write('{} {}\n'.format(job_number, result)) # the '\n' is a new line


# Then create a `submit.sh` script to run it as an Array job to fill the `results.txt` file with results.
# This is how many jobs you will need:

# In[9]:

len(sample)


# But realize that your Python script above expects the job number to start at zero, so you'll probably want something like
# ```
#     #SBATCH --array=0-7999%16
# ```
# in your batch file.
# Once your jobs have all finished, copy the `results.txt` back to your computer and put it alongside this Notebook.

# ## Importing and analyzing the results 
# Then come back here to load the results and continue the sensitivy analysis.
# Because our results file may not be in order, but contains the job number at the start of each line, we need to do a little manipulation to get the `output` array as needed

# In[ ]:

results_array = np.loadtxt("results.txt")
results_dict = dict()
for number, value in results_array:
    results_dict[int(number)] = value
results_dict
output = np.array([results_dict[i] for i in range(len(results_dict))])
output


# ### Factor Prioritisation
# 
# We'll run a sensitivity analysis to see which is the most influential parameter.
# 
# The results parameters are called **mu**, **sigma** and **mu_star**.
# 
# * **Mu** is the mean effect caused by the input parameter being moved over its range.
# * **Sigma** is the standard deviation of the mean effect.
# * **Mu_star** is the mean absolute effect.

# In[ ]:

Si = ma.analyze(morris_problem, sample, output, print_to_console=False)
print("{:20s} {:>7s} {:>7s} {:>7s}".format("Name", "mu", "mu_star", "sigma"))
for name, s1, st, mean in zip(morris_problem['names'], Si['mu'], Si['mu_star'], Si['sigma']):
    print("{:20s} {:=7.2f} {:=7.2f} {:=7.2f}".format(name, s1, st, mean))


# We can plot the results

# In[ ]:

fig, (ax1, ax2) = plt.subplots(1,2)
mp.horizontal_bar_plot(ax1, Si, param_dict={})
mp.covariance_plot(ax2, Si, {})


# In[ ]:



