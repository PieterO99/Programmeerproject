from boid_flockers.model import *
import matplotlib.pyplot as plt
import numpy as np
from mesa.batchrunner import BatchRunner

# Run the model
fixed_params = {"population": 50,
    "width": 100,
    "height": 100,
    "speed": 1,
    "vision": 30}
variable_params = {"distance_factor": [0.5, 1.0, 1.5, 2.0, 2.5]}

batch_run = BatchRunner(BoidFlockers,
                        variable_params,
                        fixed_params,
                        iterations=10,
                        max_steps=100,
                        model_reporters={"Flow": compute_flow, "Collissions": compute_collissions})
batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
#run_data.head()
print(run_data)
print(run_data.Flow)
plt.bar(run_data.distance_factor, run_data.Flow, label="Flow")
plt.bar(run_data.distance_factor, run_data.Collissions, label="Collissions")
plt.xlabel("distance_factor")
plt.ylabel("Flow / Collissions")
plt.legend(loc="upper right")

plt.savefig('flow_plot.png')

#Get the Agent DataCollection
data_collector_agents = batch_run.get_collector_agents()

#print(data_collector_agents[("eq",2)])

#Get the Model DataCollection.

data_collector_model = batch_run.get_collector_model()

"""
print(data_collector_model[("eq",1)])
print(data_collector_model[("uneq",11)])
print(data_collector_model[("std",21)])
"""