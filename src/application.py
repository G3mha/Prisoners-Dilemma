import json
import numpy as np


FILE_LOCATION = "data/data.json"


def load_repo_data(file_path):
  """
  Load repository data from the given JSON file.
  """
  try:
    with open(file_path, 'r', encoding='utf-8') as f:
      return json.load(f)
  except FileNotFoundError:
    print(f"Error: File '{file_path}' not found")
    return []
  except json.JSONDecodeError:
    print(f"Error: File '{file_path}' contains invalid JSON")
    return

def get_min_max_metrics():
  """
  Get the minimum and maximum values of the given data.
  """
  min_max_values = {
    'commits': (0, 100000),
    'contributors': (0, 10000),
    'open_pr': (0, 100000),
    'closed_pr': (0, 100000),
    'merged_pr': (0, 100000),
    'open_issue': (0, 50000),
    'closed_issue': (0, 50000),
    'stars': (0, 500000),
    'fork' : (0, 500000),
  }
  return np.array([min_max_values[metric] for metric in min_max_values])

def reward_function(x):
  """
  Reward function for the optimization problem.
  """
  correlation_with_mean = {
    'commits' : 0.11,
    'contributors' : 0.08,
    'open_pr' : 0.17,
    'closed_pr' : 0.06,
    'merged_pr' : 0.11,
    'open_issue' : 0.14,
    'closed_issue' : 0.19,
    'stars' : 0.08,
    'fork' : 0.10,
  }
  return sum([correlation_with_mean[metric] * x[i] for i, metric in enumerate(correlation_with_mean)])
