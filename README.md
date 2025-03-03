# Prisoner's Dilemma

## How the data was collected

All the data was collected through the GitHub API. The data was collected in two steps. The first step was to collect the top 1000 repositories on GitHub for contributors, chosen by their number of stars received. The second step was to collect the data for each of the top 1000 repositories.

The data was collected in a CSV file, which can be found in the data folder. The attributes collected for each repository can be found in [Contribution Metrics](#contribution-metrics) and [Activity Metrics](#activity-metrics).

### Contribution Metrics

- **unique_contributors_count**: The total number of different individuals who have contributed to the repository.

- **median_contributions_per_contributor**: The median value in the distribution of contributions, indicating the typical contribution level.

- **mean_contributions_per_contributor**: The average number of contributions per contributor.

- **contribution_gini_coefficient**: A measure of inequality in contributions, where:
  - 0: Perfect equality (everyone contributes equally)
  - 1: Perfect inequality (one person makes all contributions)
  - Values around 0.8 suggest a heavy concentration of work among a small core group

## Activity Metrics

- **total_annual_commits**: The total number of commits made to the repository over the past year.

- **average_weekly_commits**: The mean number of commits per week, indicating the typical activity level.

- **commit_consistency**: A measure of how evenly distributed commits are over time. Lower values indicate more consistent contribution patterns, while higher values suggest more sporadic development with bursts of activity.
