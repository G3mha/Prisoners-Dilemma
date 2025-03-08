import numpy as np
from algorithm import particle_swarm_optimization
from application import FILE_LOCATION, load_repo_data, get_metrics, get_metrics_ranges, get_min_max_metrics


data = load_repo_data(FILE_LOCATION)
metrics = get_metrics(data)
metrics_ranges = get_metrics_ranges(metrics)

dim = 9
bounds = get_min_max_metrics()
best_pos, best_val = particle_swarm_optimization(dim, bounds)
print("Best Position:", best_pos)
print("Best Value:", best_val)
