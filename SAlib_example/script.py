# This is a script that you should run on Discovery,
# as part of a Slurm Array job, with 1000 jobs.
import numpy as np
import os
from model import max_vehicle_power
big_parameter_list = np.loadtxt("parameter_values.txt")
job_number = int(os.getenv('SLURM_ARRAY_TASK_ID', default='0'))
assert 0<=job_number<1000, "Job number should run from 0 to 999"
for i in range(8):
    parameter_number = (8 * job_number) + i
    parameters = big_parameter_list[parameter_number]
    result = max_vehicle_power(*parameters)
    """
    Because we don't know what order the jobs will complete in,
    the results may be written out of order!
    To deal with this, we will write the job number in the results file
    as well as the result:
    """
    with open("results.txt", 'a') as result_file: # 'a' is append mode, and will add to the file.
        result_file.write('{} {}\n'.format(parameter_number, result)) # the '\n' is a new line
