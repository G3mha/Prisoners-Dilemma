import numpy as np

def normalize_parameters(params, min_values, max_values):
    """
    Normalize parameters to range [0,1] based on min and max values.
    """
    for i in range(len(params)):
        if max_values[i] == min_values[i]:
            params[i] = 0.5
        else:
            params[i] = (params[i] - min_values[i]) / (max_values[i] - min_values[i])
    return params

def sphere_fitness_function(params):
    """
    Calculate the weighted Euclidean distance (sphere fitness) between the parameters and center.
    """
    min_values = [
        1,      # unique_contributors_count: Min 1 contributor
        1,      # median_contributions_per_contributor: Min 1 contribution 
        1,      # mean_contributions_per_contributor: Min 1 contribution
        0,      # contribution_gini_coefficient: 0 = perfect equality
        1,      # total_annual_commits: Min 1 commit per year
        0.02,   # average_weekly_commits: ~1 commit per year
        0,      # commit_consistency: 0 = perfectly consistent
    ]
    
    max_values = [
        5000,   # unique_contributors_count: Accommodate larger projects
        500,    # median_contributions_per_contributor: Higher ceiling
        1000,   # mean_contributions_per_contributor: Higher ceiling for skewed distributions
        1,      # contribution_gini_coefficient: 1 = perfect inequality
        50000,  # total_annual_commits: ~1000 commits per week
        1000,   # average_weekly_commits: Higher ceiling
        10,     # commit_consistency: Higher ceiling for more variable projects
    ]

    center = [
        0.75,  # unique_contributors_count: High but not maximum (broad participation)
        0.65,  # median_contributions_per_contributor: Moderately high (sustained engagement)
        0.55,  # mean_contributions_per_contributor: Moderate (balanced contributions)
        0.25,  # contribution_gini_coefficient: Low (equal distribution of work)
        0.65,  # total_annual_commits: Moderately high (active development)
        0.55,  # average_weekly_commits: Moderate (consistent activity)
        0.35   # commit_consistency: Low to moderate (regular rather than sporadic)
    ]

    weights = [
        1.5,  # unique_contributors_count: Higher weight (broad participation)
        1.0,  # median_contributions_per_contributor: Standard weight
        1.0,  # mean_contributions_per_contributor: Standard weight
        2.0,  # contribution_gini_coefficient: Highest weight (equality of contributions)
        1.0,  # total_annual_commits: Standard weight
        1.0,  # average_weekly_commits: Standard weight
        1.3   # commit_consistency: Higher weight (consistency of cooperation)
    ]
    
    norm_params = normalize_parameters(params, min_values, max_values)
    
    # Calculate weighted Euclidean distance
    distance = np.sqrt(sum(weights[i] * (norm_params[i] - center[i])**2 for i in range(7)))
    
    return distance

