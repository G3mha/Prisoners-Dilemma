# Particle Swarm Optimization for the Prisoner's Dilemma

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

## Ethical Analysis

## How Particle Swarm Optimization Might Be Misused

The algorithm could be misused in several ways, such as:

- **Manipulate contributor behavior**: Organizations could optimize engagement metrics while minimizing actual resource allocation, creating a facade of community while extracting maximum value from contributors.

- **Corporate competitive advantage**: Large companies could strategically identify optimal non-contribution strategies that appear cooperative but actually minimize their resource commitment to open-source projects they profit from.

## Algorithmic Bias

Although unbiased in its core design, particle swarm optimization can introduce bias through the fitness function used to evaluate contributions. Those potential sources of bias include:

- **Concentration bias**: With a high contribution Gini coefficient, there's significant inequality in participation. If the algorithm optimizes strategies for this concentration, it would favor a small group of contributors, while the median contributor has far fewer contributions.

- **Activity rhythm bias**: Based on the commit consistency metrics, the algorithm might favor contributors who match existing project rhythms, potentially neglecting important contributions from those with a non-traditional work schedule.

- **Scale bias**: In a repository with hundreds of unique contributors but a small number of weekly commits, the algorithm can undervalue small but critical contributions from the majority of participants who contribute below the mean rate.

## Mitigation Strategies

These ethical concerns can be addressed through:

- **Transparent fitness functions**: Clearly document how the scores for contribution are calculated, allowing judged communities to audit and refine the metrics, as any other Open-Source project.

- **Optimization goals**: Incorporate in the future a multi-objective optimization, valuing different types of contributions (code, documentation, community support), and not just commits.

- **Regular algorithmic audits**: Periodically check if the algorithmic outcomes are fitting with the reality of the project, and its potential unusual workflow.

## Case Studies

1. **Linux Kernel Development**: The Linux Foundation's 2024 report showed that over 4,300 developers from 500 companies contributed to the kernel, with unpaid developers contributing to only 8.2% of the development. This is situation where the algorithm can concentrate development influence on corporate players, that if not carefully balanced, can hinder individual contributions.

2. **OpenSSL Heartbleed Vulnerability**: Despite securing 66% of web servers, OpenSSL was maintained by two part-time employees prior to the critical Heartbleed bug in 2014. Annual donations pre-2014 never exceeded $1 million, and with minimal code contributions. It was only after the incident that the Linux Foundation’s Core Infrastructure Initiative, addressed the systemic underfunding. It is a clear example of how algorithms focused solely on feature contributions, without contextual maintenance work or financing informating, can lead to catastrophes affecting billions of users.

## Sources

- [Linux Foundation Report 2024 Analysis](https://datacentre.solutions/news/52774/the-linux-foundation-releases-annual-kernel-development-report)

- [OpenSSL Heartbleed Vulnerability](https://www.mend.io/blog/how-the-heartbleed-vulnerability-shaped-openssl/)
