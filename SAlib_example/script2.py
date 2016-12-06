# This is a script that you should run on Discovery,
# as part of a Slurm Array job, with 100 jobs.
import numpy as np
import os
from model import max_vehicle_power
big_parameter_list = np.loadtxt("parameter_values.txt")
header = open("parameter_values.txt").readline()
header = header.strip('#\n ') # remove the '#', space, and newline from the start and end
column_names = header.split()

job_number = int(os.getenv('SLURM_ARRAY_TASK_ID', default='0'))
assert 0<=job_number<100, "Job number should run from 0 to 99"
for i in range(80):
    parameter_number = (80 * job_number) + i
    parameters = big_parameter_list[parameter_number]
    arguments_dictionary = { key:value for key, value in zip(column_names, parameters)}
    result = max_vehicle_power(**arguments_dictionary)
    print('{} {}'.format(parameter_number, result))
