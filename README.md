# Particle Swarm Optimization (PSO) for Open Source Project Analysis

Authors: [Enricco Gemha](https://github.com/G3mha), [Joseph Vazhaeparampill](https://github.com/Josephvazhae1)

## Libraries Used

- NumPy: For numerical operations and array handling
- Matplotlib: For visualization in earlier iterations (deprecated)
- Requests: For GitHub API interactions
- JSON: For data parsing and storage

## Resources Used

1. [GitHub REST API Documentation](https://docs.github.com/en/rest)
2. [Particle Swarm Optimization: Original Paper by Kennedy and Eberhart](https://ieeexplore.ieee.org/document/488968)
3. [NumPy Documentation](https://numpy.org/doc/stable/)
4. [Linux Foundation Report 2024](https://datacentre.solutions/news/52774/the-linux-foundation-releases-annual-kernel-development-report)
5. [OpenSSL Heartbleed Vulnerability](https://www.mend.io/blog/how-the-heartbleed-vulnerability-shaped-openssl/)
6. [Predicting Health Indicators for Open Source Projects (using Hyperparameter Optimization)](https://doi.org/10.48550/arXiv.2006.07240)
7. [Particle Swarm Optimization](https://www.sciencedirect.com/topics/physics-and-astronomy/particle-swarm-optimization#:~:text=Particle%20swarm%20optimization%20(PSO)%20was,bird%20flock%20or%20fish%20school.)
8. [Particle Swarm Optimisation: A Historical Review Up to the Current Developments](https://pmc.ncbi.nlm.nih.gov/articles/PMC7516836/)
9. [Optimizing Benchmark Functions using Particle Swarm Optimization PSO](https://journal.alsalam.edu.iq/index.php/ajest/article/view/494/175)

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

Particle Swarm Optimization is a metaheuristic, population-based optimization algorithm that is also classified as a swarm intelligence technique. It was originally developed by James Kennedy and Russel Eberhart to simulate social behaviour of a flock of birds looking for food. However, they soon realized its applicability to optimization problems and would later refine it with Yuhui Shi to create a technique for solving optimization problems.

Because it does not rely on gradient descent, it can be applied to a wide variety of problems, including those that have non-differentiable or non-continuous reward functions. It also has faster convergence compared to most genetic algorithms since it leverages direct communication between the particles instead of evolutionary selection and is relatively simple computationally only requiring position and velocity updates. Unlike simulated annealing, which follows only a single solution path, particle swarm optimization makes use of collective learning with data from each of its particles. For these reasons, it has since been widely adopted in a large variety of spaces including engineering, artificial intelligence and finance.

However, particle swarm does come with its fair share of shortcomings. The swarm can often converge to local optimums rather than absolute ones due to its heuristic nature, particular if the parameters are not effectively tuned. For instance, a larger swarm size ($N$) provides a better global search but also increases the computational cost. Inertia weight ($w$) controls how much a particle retains its previous velocity, which is useful early in the search to promote exploration, but not nearly as helpful later in the search when trying to refine the solution. Then there are the cognitive and social learning factors, $c_1$ and $c_2$. The cognitive factor $c_1$ encourages individual exploration, while the $c_2$ factor encourages group convergence. Stopping criteria could also have a large impact on the effectiveness of the algorithm. If there are not enough timesteps, the particle swarm might not find the global optimum, but a local one. Additionally, in solution spaces with higher dimensionality, finding the optimum solution becomes more and more computationally expensive and time-intensive.

## Walkthrough

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

Here is a visualization of PSO optimizing a Rastrigin function (a non-convex function with many local maxima often used as a performance test for optimization algorithms):

![image](https://github.com/user-attachments/assets/c5db9883-fc09-4557-8d04-e1f8e6143caa)

For x ∈ [−5.12, 5.12] and y ∈ [−5.12, 5.12], Rastrigin has a global maxima around x = 4.52299366 and y = 4.52299366.

Our particle swarm implementation over 100 timesteps found the global maxima to be x = 4.19189874 and y = 4.31836399.

Here is a visualization of that implementation: [Rastrigin function in 2D space graph](https://github.com/user-attachments/assets/f5412532-3587-4027-9cc9-fcfa86d1f1e6)

## Solving a Problem

### About the Problem



### Parameter Space and Optimization Bounds

Our PSO algorithm searches through a bounded parameter space representing key GitHub repository metrics. These bounds were determined through analysis of our dataset to create a realistic optimization space:

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

### How Data was Collected

All the data was collected through the GitHub API. The data was collected in two steps. The first step was to collect the top 20 repositories on GitHub for contributors, chosen by their number of stars received. The second step was to collect the data for each of the top 20 repositories.

The data was collected in a CSV file, which can be found in the data folder. The attributes collected for each repository can be found in [Contribution Metrics](#contribution-metrics) and [Activity Metrics](#activity-metrics).

### Contribution Metrics

- **unique_contributors_count**: The total number of different individuals who have contributed to the repository.

- **median_contributions_per_contributor**: The median value in the distribution of contributions, indicating the typical contribution level.

- **mean_contributions_per_contributor**: The average number of contributions per contributor.

### Activity Metrics

- **average_weekly_commits**: The mean number of commits per week, indicating the typical activity level.

- **commit_consistency**: A measure of how evenly distributed commits are over time. Lower values indicate more consistent contribution patterns, while higher values suggest more sporadic development with bursts of activity.

### Reward Function Implementation

For our implementation, we created a reward function that evaluates repository health based on weighted metrics including **commits**, **contributors**, **PRs**, **issues**, **stars**, and **forks**. Each metric is normalized and weighted according to its correlation with project success, with higher weights assigned to metrics like closed issues (0.19) and open PRs (0.17) that more strongly indicate active development and community engagement. These weight values are based on the paper (6).

## Ethical Analysis

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

### Case Studies

1. **Linux Kernel Development**: The Linux Foundation's 2024 report showed that over 4,300 developers from 500 companies contributed to the kernel, with unpaid developers contributing to only 8.2% of the development (4). This is situation where the algorithm can concentrate development influence on corporate players, that if not carefully balanced, can hinder individual contributions.

2. **OpenSSL Heartbleed Vulnerability**: Despite securing 66% of web servers, OpenSSL was maintained by two part-time employees prior to the critical Heartbleed bug in 2014. Annual donations pre-2014 never exceeded $1 million, and with minimal code contributions. It was only after the incident that the Linux Foundation's Core Infrastructure Initiative, addressed the systemic underfunding (5). It is a clear example of how algorithms focused solely on feature contributions, without contextual maintenance work or financing informating, can lead to catastrophes affecting billions of users.
