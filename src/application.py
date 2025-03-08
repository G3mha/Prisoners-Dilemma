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

def get_metrics(data):
  """
  Get repository data from the JSON file.
  """
  result = []
  for repo_data in data:
    if not repo_data["unique_contributors_count"]:
      print(f"Error: 'unique_contributors_count' not found in repository {repo_data['full_name']}")
      continue
    result.append({
      "unique_contributors_count": repo_data["unique_contributors_count"],
      "median_contributions_per_contributor": repo_data["median_contributions_per_contributor"],
      "mean_contributions_per_contributor": repo_data["mean_contributions_per_contributor"],
      "average_weekly_commits": repo_data["average_weekly_commits"],
      "commit_consistency": repo_data["commit_consistency"],
    })
  return result

def get_metrics_ranges(metrics):
  """
  Get the range of repository data.
  """
  return {
    "unique_contributors_count": (min([repo["unique_contributors_count"] for repo in metrics]), max([repo["unique_contributors_count"] for repo in metrics])),
    "median_contributions_per_contributor": (min([repo["median_contributions_per_contributor"] for repo in metrics]), max([repo["median_contributions_per_contributor"] for repo in metrics])),
    "mean_contributions_per_contributor": (min([repo["mean_contributions_per_contributor"] for repo in metrics]), max([repo["mean_contributions_per_contributor"] for repo in metrics])),
    "average_weekly_commits": (min([repo["average_weekly_commits"] for repo in metrics]), max([repo["average_weekly_commits"] for repo in metrics])),
    "commit_consistency": (min([repo["commit_consistency"] for repo in metrics]), max([repo["commit_consistency"] for repo in metrics])),
  }

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
