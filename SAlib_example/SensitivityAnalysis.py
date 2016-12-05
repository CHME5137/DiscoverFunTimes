
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


# ### One-at-time approach
# 
# First, we're going to try the **one-at-a-time** (OAT) approach.
# 
# Find the sliders in the example which are set up for the parameters of the Nissan Leaf.

# In[5]:

@interact(connector=widgets.FloatSlider(value=2.3, min=2.3, max=22, step=0.5), 
          battery_size=widgets.FloatSlider(value=24, min=10, max=100, step=5), 
          distance_driven=widgets.FloatSlider(value=0, min=0, max=100, step=5), 
          range_buffer=widgets.FloatSlider(value=0, min=0, max=100, step=10),
          dispatch_time=widgets.FloatSlider(value=1.4, min=0.5, max=24, step=0.5))
def plot_power(connector, battery_size, distance_driven, range_buffer, dispatch_time):
    power = max_vehicle_power(connector,
                      battery_size,
                      distance_driven,
                      range_buffer,
                      dispatch_time
                      )
    return print("The maximum power is {} kW".format(round(power, 2)))


# In[6]:

def monte_carlo_large(data):
    dispatch_time = 4
    y = max_vehicle_power(data[0], data[1], data[2], data[3], data[6], data[4], data[5])
    return y


# # Using SALib to run a Sensitivity Analysis
# 
# SALib is a **free** **open-source** **Python** library
# 
# If you use Python, you can install it by running the command
# 
# ```python
# pip install SALib
# ```
# 
# [Documentation](http://salib.readthedocs.org/) is available online and you can also view the code on [Github](http://salib.github.io/SALib/).
# 
# The library includes:
# * Sobol Sensitivity Analysis ([Sobol 2001](http://www.sciencedirect.com/science/article/pii/S0378475400002706), [Saltelli 2002](http://www.sciencedirect.com/science/article/pii/S0010465502002801), [Saltelli et al. 2010](http://www.sciencedirect.com/science/article/pii/S0010465509003087))
# * Method of Morris, including groups and optimal trajectories ([Morris 1991](http://www.tandfonline.com/doi/abs/10.1080/00401706.1991.10484804), [Campolongo et al. 2007](http://www.sciencedirect.com/science/article/pii/S1364815206002805))
# * Fourier Amplitude Sensitivity Test (FAST) ([Cukier et al. 1973](http://scitation.aip.org/content/aip/journal/jcp/59/8/10.1063/1.1680571), [Saltelli et al. 1999](http://amstat.tandfonline.com/doi/abs/10.1080/00401706.1999.10485594))
# * Delta Moment-Independent Measure ([Borgonovo 2007](http://www.sciencedirect.com/science/article/pii/S0951832006000883), [Plischke et al. 2013](http://www.sciencedirect.com/science/article/pii/S0377221712008995))
# * Derivative-based Global Sensitivity Measure (DGSM) ([Sobol and Kucherenko 2009](http://www.sciencedirect.com/science/article/pii/S0378475409000354))
# * Fractional Factorial Sensitivity Analysis ([Saltelli et al. 2008](http://www.wiley.com/WileyCDA/WileyTitle/productCd-0470059974.html))
# 

# ### Import the package

# In[7]:

from SALib.sample import morris as ms
from SALib.analyze import morris as ma
from SALib.plotting import morris as mp


# ### Define a problem file
# 
# In the code below, a problem file is used to define the variables we wish to explore

# In[8]:

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

# In[10]:

number_of_trajectories = 1000
sample = ms.sample(morris_problem, number_of_trajectories, num_levels=4, grid_jump=2)
print("The sample array is ",sample.shape)
print("Here are the first 10 rows:")
for j in range(10):
    print(' '.join(['{:10.3f}'.format(i) for i in sample[j]]))


# ### Factor Prioritisation
# 
# We'll run a sensitivity analysis of the power module to see which is the most influential parameter.
# 
# The results parameters are called **mu**, **sigma** and **mu_star**.
# 
# * **Mu** is the mean effect caused by the input parameter being moved over its range.
# * **Sigma** is the standard deviation of the mean effect.
# * **Mu_star** is the mean absolute effect.

# In[31]:

# Run the sample through the monte carlo procedure of the power model
output = monte_carlo_large(sample.T)
# Store the results for plotting of the analysis
Si = ma.analyze(morris_problem, sample, output, print_to_console=False)
print("{:20s} {:>7s} {:>7s} {:>7s}".format("Name", "mu", "mu_star", "sigma"))
for name, s1, st, mean in zip(morris_problem['names'], Si['mu'], Si['mu_star'], Si['sigma']):
    print("{:20s} {:=7.2f} {:=7.2f} {:=7.2f}".format(name, s1, st, mean))


# We can plot the results

# In[33]:

fig, (ax1, ax2) = plt.subplots(1,2)
mp.horizontal_bar_plot(ax1, Si, param_dict={})
mp.covariance_plot(ax2, Si, {})


# ## A More Complicated Example
# 
# Lets look at a more complicated example.  This now integrates the previous power module into a simple cost-benefit analysis.
# 
# Trying to work out anything with all those sliders is pretty difficult.  We need to strip out the uneccesssary parameters and focus our efforts on the influential inputs.

# In[34]:

@interact(battery_size=widgets.FloatSlider(value=24, min=10, max=100, step=5), 
          battery_unit_cost=widgets.FloatSlider(value=350, min=100, max=400, step=50),
          connector_power=widgets.FloatSlider(value=2.3, min=2.3, max=22, step=0.5), 
          lifetime_cycles=widgets.FloatSlider(value=2000, min=1000, max=10000, step=1000),
          depth_of_discharge=widgets.FloatSlider(value=0.8, min=0.5, max=1.0, step=0.1),
          electricity_price=widgets.FloatSlider(value=0.1, min=0.01, max=0.5, step=0.01),
          purchased_energy_cost=widgets.FloatSlider(value=0.1, min=0.01, max=0.5, step=0.01),
          capacity_price=widgets.FloatSlider(value=0.007, min=0.001, max=0.01, step=0.001),
          round_trip_efficiency=widgets.FloatSlider(value=0.73, min=0.50, max=1.0, step=0.01),
          cost_of_v2g_equip=widgets.FloatSlider(value=2000, min=100, max=5000, step=100),
          discount_rate=widgets.FloatSlider(value=0.10, min=0.0, max=0.2, step=0.01),
          economic_lifetime=widgets.FloatSlider(value=10, min=3, max=25, step=1),
          ratio_dispatch_to_contract=widgets.FloatSlider(value=0.10, min=0.01, max=0.50, step=0.01),
          distance_driven=widgets.FloatSlider(value=0, min=0, max=100, step=5), 
          range_buffer=widgets.FloatSlider(value=0, min=0, max=100, step=10),
          hours_connected_per_day=widgets.FloatSlider(value=18, min=0.5, max=24, step=0.5))
def plot_profit(battery_size,
                battery_unit_cost,
                connector_power,
                lifetime_cycles,
                depth_of_discharge,
                electricity_price,
                purchased_energy_cost,
                capacity_price,
                round_trip_efficiency,
                cost_of_v2g_equip,
                discount_rate,
                economic_lifetime,
                distance_driven,
                range_buffer,
                ratio_dispatch_to_contract,
                hours_connected_per_day):
    profit, revenue, cost = compute_profit(
                                            battery_size,
                                            battery_unit_cost,
                                            connector_power,
                                            lifetime_cycles,
                                            depth_of_discharge,
                                            electricity_price,
                                            purchased_energy_cost,
                                            capacity_price,
                                            round_trip_efficiency,
                                            cost_of_v2g_equip,
                                            discount_rate,
                                            economic_lifetime,
                                            distance_driven,
                                            range_buffer,
                                            ratio_dispatch_to_contract,
                                            hours_connected_per_day
                                            )
    return print("Profit £{} = £{} - £{}".format(np.round(profit,2), np.round(revenue, 2), np.round(cost,2) ))


# ### Factor Fixing
# 
# We'll perform a **factor fixing** sensitivity analysis using a different method - that of Sobol.

# In[35]:

from SALib.sample.saltelli import sample as ss
from SALib.analyze.sobol import analyze as sa

problem = {
    # There are sixteen variables
    'num_vars': 16,
    # These are their names
    'names': ['battery_size',
              'battery_unit_cost',
              'connector_power',
              'lifetime_cycles',
              'depth_of_discharge',
              'electricity_price',
              'purchased_energy_cost',
              'capacity_price',
              'round_trip_efficiency',
              'cost_of_v2g_equip',
              'discount_rate',
              'economic_lifetime',
              'distance_driven',
              'range_buffer',
              'ratio_dispatch_to_contract',
              'hours_connected_per_day'],
    # These are their plausible ranges over which we'll move the variables
    'bounds': [       
                [10, 100],
                [100, 400],
                [2.3, 22],
                [1000, 10000],
                [0.5, 1.0],
                [0.01, 0.2], 
                [0.01, 0.2],
                [0.001, 0.01], 
                [0.65, 1.0],
                [100, 5000],
                [0.0, 0.2], 
                [3, 25],
                [0, 100], 
                [0, 100], 
                [0.01, 0.50],
                [0.5, 24],
              ],
    # I don't want to group any of these variables together
    'groups': None
    }


# In[36]:

sample = ss(problem, 1000, calc_second_order=False)
profit, revenue, cost = compute_profit(sample[:,0], sample[:,1], sample[:,2], sample[:,3], sample[:,4], sample[:,5], sample[:,6]
                       , sample[:,7], sample[:,8], sample[:,9], sample[:,10], sample[:,11], sample[:,12], sample[:,13]
                       , sample[:,14], sample[:,15])
SI = sa(problem, profit, calc_second_order=False, print_to_console=False)
print("{:28s} {:>5s} {:>5s} {:>12s}".format("Name", "1st", "Total", "Mean of Input"))
for name, s1, st, mean in zip(problem['names'], SI['S1'], SI['ST'], sample.mean(axis=0)):
    print("{:28s} {:=5.2f} {:=5.2f} ({:=12.2f})".format(name, s1, st, mean))


# In[42]:

print(sample.shape)
for j in range(18):
    print(' '.join(['{:.3f}'.format(i) for i in sample[j]]))


# The results show that the most important parameters are:
# * Capital cost of the V2G equipment
# * Ratio of dispatch to contract
# * Battery size
# * Economic lifetime
# * Purchased energy cost
# 
# Other comments:
# * __Lifetime cycles__ has a reasonably important first order effect so we can include that too.
# * __Battery size__ has much more important interaction effects than first-order effects
# * Same for __Purchased_energy_cost__
# 
# We can now fix the other parameters and revisit our slider model to perform some analysis.

# In[37]:

@interact(battery_size=widgets.FloatSlider(value=70, min=10, max=100, step=5), 
          purchased_energy_cost=widgets.FloatSlider(value=0.1, min=0.01, max=0.5, step=0.01),
          cost_of_v2g_equip=widgets.FloatSlider(value=2000, min=100, max=5000, step=100),
          economic_lifetime=widgets.FloatSlider(value=10, min=3, max=25, step=1),
          ratio_dispatch_to_contract=widgets.FloatSlider(value=0.10, min=0.01, max=0.50, step=0.01),
         lifetime_cycles=widgets.FloatSlider(value=2000, min=1000, max=10000, step=500))
def plot_profit(battery_size,
                purchased_energy_cost,
                cost_of_v2g_equip,
                economic_lifetime,
                ratio_dispatch_to_contract,
                lifetime_cycles):
    profit, revenue, cost = compute_profit( lifetime_cycles=lifetime_cycles,
                                            battery_size=battery_size,
                                            purchased_energy_cost=purchased_energy_cost,
                                            cost_of_v2g_equip=cost_of_v2g_equip,
                                            economic_lifetime=economic_lifetime,
                                            ratio_dispatch_to_contract=ratio_dispatch_to_contract
                                            )
    return print("Profit £{} = £{} - £{}".format(np.round(profit,2), np.round(revenue, 2), np.round(cost,2) ))


# # Summary
# 
# 
# Sensitivity analysis helps you:
# * Think through your assumptions
# * Quantify uncertainty
# * Focus on the most influential uncertainties first
# * Learn [Python](https://www.python.org)
# 
# Similar packages to [SALib]() for other languages/programmes:
# * [Matlab Toolbox **SAFE** for GSA](http://www.sciencedirect.com/science/article/pii/S1364815215001188)
# * [`sensitivity` package for R](https://cran.r-project.org/web/packages/sensitivity/index.html)
# * [Excel](http://crossfitjerseycity.org/wp-content/uploads/2015/01/keep-calm-and-good-luck-graphic1.png)

# In[45]:

print('for {} dimension, {} is within 10% of the edge'.format(1,0.2))


# In[49]:

for i in range(100):
    
    f = 1.-(0.8 **i)
    print('for {} dimension, {:.2f} is within 10% of the edge'.format(i,f))


# In[ ]:



