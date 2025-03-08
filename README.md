# Particle Swarm Optimization (PSO) for Open Source Project Analysis

Authors: [Enricco Gemha](https://github.com/G3mha), [Joseph Vazhaeparampill](https://github.com/Josephvazhae1)

## Introduction

This project implements Particle Swarm Optimization (PSO) to analyze open source contribution patterns as a solution to the prisoner's dilemma in open source development on GitHub repositories. By modeling how various metrics correlate with project health and sustainability, we identify the best repositories to invest time and effort in contributing to.

## Table of Contents

- [Libraries Used](#libraries-used)
- [Resources Used](#resources-used)
- [Installation and Setup](#installation-and-setup)
- [Project Structure](#project-structure)
- [Background of Algorithm](#background-of-algorithm)
- [How the Algorithm Works](#how-the-algorithm-works)
- [Solving a Problem](#solving-a-problem)
  - [Open Source Contribution as a Prisoner's Dilemma](#open-source-contribution-as-a-prisoners-dilemma)
  - [How PSO Can Help](#how-pso-can-help)
  - [How Data was Collected](#how-data-was-collected)
  - [Metrics](#metrics)
    - [Contribution Metrics](#contribution-metrics)
    - [Issue Management Metrics](#issue-management-metrics)
    - [Community Engagement Metrics](#community-engagement-metrics)
  - [Optimization Bounds](#optimization-bounds)
  - [Reward Function Implementation](#reward-function-implementation)
- [Ethical Analysis](#ethical-analysis)
  - [How Particle Swarm Optimization Might Be Misused](#how-particle-swarm-optimization-might-be-misused)
  - [Algorithmic Bias](#algorithmic-bias)
  - [Mitigation Strategies](#mitigation-strategies)
  - [Case Studies](#case-studies)

## Libraries Used

- NumPy: For numerical operations and array handling
- Matplotlib: For visualization in earlier iterations (deprecated)
- Requests: For GitHub API interactions
- JSON: For data parsing and storage

## Resources Used

[1] GitHub, "REST API Documentation," GitHub Docs. [Online]. Available: https://docs.github.com/en/rest. [Accessed: Mar. 8, 2025].

[2] J. Kennedy and R. Eberhart, "Particle swarm optimization," in Proceedings of ICNN'95 - International Conference on Neural Networks, Perth, WA, Australia, 1995, pp. 1942-1948.

[3] X. Wang, S. Lv, and J. Quan, "The evolution of cooperation in the Prisoner's Dilemma and the Snowdrift game based on Particle Swarm Optimization," Physica A: Statistical Mechanics and its Applications, vol. 482, pp. 286-295, 2017, doi: 10.1016/j.physa.2017.04.080.

[4] The Linux Foundation, "The Linux Foundation Releases Annual Kernel Development Report," Datacentre Solutions, 2024. [Online]. Available: https://datacentre.solutions/news/52774/the-linux-foundation-releases-annual-kernel-development-report. [Accessed: Mar. 8, 2025].

[5] Mend, "How the Heartbleed Vulnerability Shaped OpenSSL," Mend.io, 2023. [Online]. Available: https://www.mend.io/blog/how-the-heartbleed-vulnerability-shaped-openssl/. [Accessed: Mar. 8, 2025].

[6] T. Xia, W. Fu, R. Shu, R. Agrawal, and T. Menzies, "Predicting Health Indicators for Open Source Projects (using Hyperparameter Optimization)," arXiv:2006.07240, Jun. 2020.

[7] M. Sahimi and P. Tahmasebi, "Reconstruction, optimization, and design of heterogeneous materials and media: Basic principles, computational algorithms, and applications," Physics Reports, vol. 939, pp. 1-82, 2021, doi: 10.1016/j.physrep.2021.09.003.

[8] D. Freitas, L. G. Lopes, and F. Morgado-Dias, "Particle Swarm Optimisation: A Historical Review Up to the Current Developments," Entropy, vol. 22, no. 3, p. 362, Mar. 2020, doi: 10.3390/e22030362.

[9] B. K. Abbas, Q. A. Z. Jabbar, and R. T. Hameed, "Optimizing Benchmark Functions using Particle Swarm Optimization PSO," Al-Salam Journal for Engineering and Technology, vol. 4, no. 1, pp. 192-198, 2025, doi: 10.55145/ajest.2025.04.01.019.

[10] G. Papazoglou and P. Biskas, "Review and Comparison of Genetic Algorithm and Particle Swarm Optimization in the Optimal Power Flow Problem," Energies, vol. 16, no. 3, p. 1152, 2023, doi: 10.3390/en16031152.

[11] M. A. K. Azrag and T. A. A. Kadir, "Empirical Study of Segment Particle Swarm Optimization and Particle Swarm Optimization Algorithms," International Journal of Advanced Computer Science and Applications, vol. 10, no. 8, pp. 480-485, 2019, doi: 10.14569/IJACSA.2019.0100863.

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/G3mha/particle-swarm-optimization-prisoners-dilemma.git
   cd particle-swarm-optimization-prisoners-dilemma
   ```

2. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the main script:

   ```bash
   python src/main.py
   ```

## Project Structure

- `src/`: Source code directory
  - `algorithm.py`: Core PSO implementation
  - `application.py`: Application logic for repository analysis
  - `helpers.py`: Utility functions
  - `main.py`: Entry point for running the analysis
- `data/`: Contains repository data
  - `data.json`: Structured repository metrics
  - `data.csv`: CSV version of repository metrics
- `requirements.txt`: Required Python dependencies
- `deprecated/`: Earlier implementations and experiments
  - `ParticleSwarm.py`: Initial PSO implementation
  - `ParticleSwarm_RastriginAnimation.py`: Visualization of PSO on Rastrigin function
- `github-api/`: Scripts for data collection
  - `collector.py`: GitHub API interaction code

## Background of Algorithm

Particle Swarm Optimization (PSO) is a metaheuristic, population-based optimization algorithm that is also classified as a swarm intelligence technique. It was originally developed by James Kennedy and Russel Eberhart [2] to simulate social behaviour of a flock of birds looking for food. However, they soon realized its applicability to optimization problems and would later refine it with Yuhui Shi to create a technique for solving optimization problems.

Because it does not rely on gradient descent, it can be applied to a wide variety of problems, including those that have non-differentiable or non-continuous reward functions. It also has faster convergence compared to most Genetic Algorithms (GA) since it leverages direct communication between the particles instead of evolutionary selection and is relatively simple computationally only requiring position and velocity updates. Having less parameters to tune than the GA, the PSO is simpler to implement, as suggested by the paper [10]. Unlike simulated annealing, which follows only a single solution path, particle swarm optimization makes use of collective learning with data from each of its particles. For these reasons, it has since been widely adopted in a large variety of spaces including engineering, artificial intelligence and finance.

However, particle swarm does come with its fair share of shortcomings. The swarm can often converge to local optimums rather than absolute ones due to its heuristic nature, particular if the parameters are not effectively tuned. For instance, a larger swarm size ($N$) provides a better global search but also increases the computational cost. Inertia weight ($w$) controls how much a particle retains its previous velocity, which is useful early in the search to promote exploration, but not nearly as helpful later in the search when trying to refine the solution. Then there are the cognitive and social learning factors, $c_1$ and $c_2$. The cognitive factor $c_1$ encourages individual exploration, while the $c_2$ factor encourages group convergence. Stopping criteria could also have a large impact on the effectiveness of the algorithm. If there are not enough timesteps, the particle swarm might not find the global optimum, but a local one. Additionally, in solution spaces with higher dimensionality, finding the optimum solution becomes more and more computationally expensive and time-intensive.

## How the Algorithm Works

The steps of the Particle Swarm Optimization algorithm are as follows, based on the paper [8]:

1. **Initialize the Swarm**:
   - Define the number of particles $N$
   - Randomly initialize each particle's position $x_i$, $y_i$, $z_i$ ... (depending on the dimensionality of the solution space)
   - Randomly initialize each particle's velocity $v_i$

2. **Set Parameters**:
   - Inertia weight $w$
   - Cognitive coefficient $c_1$
   - Social coefficient $c_2$

3. **Evaluate Fitness** for each particle based on the objective function

4. **Identify Personal Best**: Track the best position each particle has achieved so far

5. **Identify Global Best**: Track the best position any particle has achieved so far

6. **Update Velocity and Position**:

   Velocity update: $$v_{i+1} = w v_i + c_1 r_1 (p_i - x_i) + c_2 r_2 (g - x_i)$$

   Position update: $$x_{i+1} = x_i + v_{i+1}$$

   Where:
   - $w$ is the inertia weight
   - $c_1$ & $c_2$ are acceleration coefficients
   - $r_1$ & $r_2$ are random numbers between 0 & 1
   - $p_i$ is the personal best position
   - $g$ is the global best position

7. **Apply Constraints** to ensure particles stay within the solution space

8. **Repeat Steps 3-7** until a stopping criterion is met:
   - Maximum number of iterations reached
   - Improvement in the global best fitness is below a threshold

9. **Return Result**: The global best position g as the best approximation to the optimal solution

Based on the concept proposed by the paper [11], here is a visualization of PSO optimizing a Rastrigin function (a non-convex function with many local maxima often used as a performance test for optimization algorithms):

![image](https://github.com/user-attachments/assets/c5db9883-fc09-4557-8d04-e1f8e6143caa)

For x ∈ [−5.12, 5.12] and y ∈ [−5.12, 5.12], Rastrigin has a global maxima around x = 4.52299366 and y = 4.52299366.

Our particle swarm implementation over 100 timesteps found the global maxima to be x = 4.19189874 and y = 4.31836399.

Here is a visualization of that implementation: [Rastrigin function in 2D space graph](https://github.com/user-attachments/assets/f5412532-3587-4027-9cc9-fcfa86d1f1e6)

## Solving a Problem

### Open Source Contribution as a Prisoner's Dilemma

Open source development presents a classic prisoner's dilemma: while everyone benefits when contributors invest time and resources into projects, individual contributors face incentives to free-ride on others' work without contributing themselves. This creates a fundamental tension:

1. **Collective benefit**: The community gains most when many participants contribute actively, and regularly to open source projects.
2. **Individual incentive**: Contributors must balance personal investment (time and effort) against uncertain returns, which can lead to under-contribution.

In organizations using open source software, they strategically decide how much to contribute versus how much to simply consume. Companies might recognize the benefit of contributing but still choose minimal engagement, so they can maximize their resources, leading to a potential "tragedy of the commons", in which very important projects become under-maintained.

### How PSO Can Help

The paper [3] suggests that the Particle Swarm Optimization algorithm can be used to solve a Prisoner's Dilemma problem. From that, in the context of our problem, open source contribution, we identified that PSO can identify an optimal contribution pattern. The algorithm searches the parameter space of key metrics like commits, issues, and pull requests to find the equilibrium point where both communities and individual contributors benefit sustainably. By using real repository data, PSO reveals which contribution patterns lead to healthier projects over time, inherently advising those seeking to invest time and effort into contributing to a repository to avoid the aforementioned "tragedy of the commons".

### How Data was Collected

The open source repository data was collected using the GitHub REST API [1]. Our collection process targeted the top 20 repositories ranked by stars, providing a representative sample of popular projects.

The data collection was executed in two phases. First, we queried the API to identify the top starred repositories. Second, for each repository, the API calls gathered metrics, which are described in the [Metrics](#metrics) section.

To handle GitHub API rate limits, it is recommended to use a personal access token. This token can be generated in the GitHub settings and passed as an environment variable to the script.

The raw data was stored in both JSON and CSV formats to allow for flexible visualization and analysis.

### Metrics

Based on the paper [6], which proposed metrics to evaluate the health of GitHub repositories, and later analysed the correlation between them and the median value. From that we divided the metrics on three categories: **Contribution Metrics**, **Issue Management Metrics**, and **Community Engagement Metrics**.

#### Contribution Metrics

- **Commits**: Total number of code changes merged into the repository. This metric indicates the overall development activity.
- **Contributors**: Count of unique developers who have contributed to the codebase. A healthy project typically has a diverse contributor base.
- **Open Pull Requests**: Current work in progress awaiting review. This shows ongoing development interest.
- **Closed Pull Requests**: Completed code submissions that were not merged. This can indicate code quality standards.
- **Merged Pull Requests**: Successfully integrated code contributions. This metric shows completed development work.

#### Issue Management Metrics

- **Open Issues**: Current problems, feature requests, and tasks awaiting resolution. This reflects both community engagement and maintenance backlog.
- **Closed Issues**: Resolved problems and completed requests. This shows responsiveness to user feedback.

#### Community Engagement Metrics

- **Stars**: Users who have bookmarked the repository. This primarily indicates popularity and perceived value.
- **Forks**: Copies of the repository created by users for their own purposes. This shows practical utility and adaptation.

### Optimization Bounds

Our PSO algorithm searches through a bounded parameter space representing key GitHub repository metrics. These bounds were determined arbitrarily by manual observation of the range of values in top GitHub repositories, ensuring sufficient space to explore potential optimal configurations.

| Metric | Minimum Value | Maximum Value |
|--------|--------------|--------------|
| Commits | 0 | 100,000 |
| Contributors | 0 | 10,000 |
| Open PRs | 0 | 100,000 |
| Closed PRs | 0 | 100,000 |
| Merged PRs | 0 | 100,000 |
| Open Issues | 0 | 50,000 |
| Closed Issues | 0 | 50,000 |
| Stars | 0 | 500,000 |
| Forks | 0 | 500,000 |

These bounds reflect the actual range observed in top GitHub repositories, especially the most popular ones, while allowing the algorithm sufficient space to explore potential optimal configurations.

### Reward Function Implementation

We created a reward function that evaluates repository health based on weighting the metrics described in the [Metrics](#metrics) section. Each metric is assigned a weight according to its correlation with project success, based on the conclusions made by the paper [6].

```python
correlation_with_mean = {
  'commits': 0.11,
  'contributors': 0.08,
  'open_pr': 0.17,
  'closed_pr': 0.06,
  'merged_pr': 0.11,
  'open_issue': 0.14,
  'closed_issue': 0.19,
  'stars': 0.08,
  'fork': 0.10,
}
```

Higher weights are assigned to metrics like closed issues (0.19) and open PRs (0.17), which can indicate a correlation with active development and community engagement. In this way, ongoing maintenance is prioritized over raw popularity indicators.

## Ethical Analysis

### Case Studies

1. **Linux Kernel Development**: The Linux Foundation's 2024 report showed that over 4,300 developers from 500 companies contributed to the kernel, with unpaid developers contributing to only 8.2% of the development [4]. This is situation where the algorithm can concentrate development influence on corporate players, that if not carefully balanced, can hinder individual contributions.

2. **OpenSSL Heartbleed Vulnerability**: Despite securing 66% of web servers, OpenSSL was maintained by two part-time employees prior to the critical Heartbleed bug in 2014. Annual donations pre-2014 never exceeded $1 million, and with minimal code contributions. It was only after the incident that the Linux Foundation's Core Infrastructure Initiative, addressed the systemic underfunding [5]. It is a clear example of how algorithms focused solely on feature contributions, without contextual maintenance work or financing informating, can lead to catastrophes affecting billions of users.

### How Particle Swarm Optimization Might Be Misused

The algorithm could be misused in several ways, such as:

- **Manipulate contributor behavior**: Organizations could optimize engagement metrics while minimizing actual resource allocation, creating a facade of community while extracting maximum value from contributors.

- **Corporate competitive advantage**: Large companies could strategically identify optimal non-contribution strategies that appear cooperative but actually minimize their resource commitment to open-source projects they profit from.

### Algorithmic Bias

Although unbiased in its core design, particle swarm optimization can introduce bias through the fitness function used to evaluate contributions. Those potential sources of bias include:

- **Concentration bias**: With a high contribution by few contributors, there's significant inequality in participation. If the algorithm optimizes strategies for this concentration, it would favor a small group of contributors, while the median contributor has far fewer contributions.

- **Activity rhythm bias**: Based on the commit consistency metrics, the algorithm might favor contributors who match existing project rhythms, potentially neglecting important contributions from those with a non-traditional work schedule.

- **Scale bias**: In a repository with hundreds of unique contributors but a small number of weekly commits, the algorithm can undervalue small but critical contributions from the majority of participants who contribute below the mean rate.

- **Fitness function bias**: The fitness function used to evaluate the contribution parameters can introduce bias if the weights between each features are not properly balanced, or key features are not accounted for. For example, the function can only considers code commits, neglecting other essential contributions like documentation or community support. Another example is the function being too heavily weighted towards the number of commits, incentivizing quantity-over-quality contributions.

### Mitigation Strategies

These ethical concerns can be addressed through:

- **Transparent reward function**: Clearly document how the scores for contribution are calculated, allowing judged communities to audit and refine the metrics, as any other Open-Source project.

- **Optimization goals**: Futurely, extend the data analysis to better consider the correlations between each feature (forks, commits, PRs, etc.) and the project's success, to ensure the algorithm is even closer to reality.

- **Regular algorithmic audits**: Periodically check if the algorithmic outcomes are fitting with the current state of the top projects, and their potential unusual workflow.

- **Diverse data sources**: Include repositories from different domains, sizes, and governance models to reduce selection bias, larger repos does not always mean better.

- **Context-aware metrics**: Implement qualitative metrics to account for project maturity, scope, and domain-specific contribution patterns.
