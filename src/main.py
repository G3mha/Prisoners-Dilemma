import json
import numpy as np
from application import load_repo_data, get_min_max_metrics, reward_function
from algorithm import particle_swarm_optimization
from helpers import normalize

def compare_repos_to_optimal(repos, optimal_position, bounds):
    """Compare actual repositories to the optimal repository found by PSO"""
    metrics = ['commits', 'contributors', 'open_pr', 'closed_pr', 
               'merged_pr', 'open_issue', 'closed_issue', 'stars', 'fork']
    
    repo_scores = []
    
    for repo in repos:
        repo_metrics = []
        for metric in metrics:
            repo_metrics.append(repo.get(metric, 0))
        
        repo_reward = reward_function(repo_metrics)
        
        squared_diffs = []
        for i, metric in enumerate(metrics):
            min_val, max_val = bounds[i]
            norm_optimal = normalize(optimal_position[i], min_val, max_val)
            norm_actual = normalize(repo_metrics[i], min_val, max_val)
            squared_diffs.append((norm_optimal - norm_actual) ** 2)
        
        distance = np.sqrt(sum(squared_diffs))
        
        repo_scores.append({
            'name': repo['name'],
            'full_name': repo['full_name'],
            'reward': repo_reward,
            'distance': distance,
            'metrics': {metric: repo.get(metric, 0) for metric in metrics}
        })
    
    return repo_scores


def print_repo_details(repo, optimal_position, metrics):
    """Print detailed metrics for a repository compared to the optimal"""
    print(f"Repository: {repo['name']} ({repo['full_name']})")
    print(f"Reward value: {repo['reward']:.2f}")
    print(f"Distance to optimal: {repo['distance']:.4f}")
    print("Metrics:")
    
    for i, metric in enumerate(metrics):
        actual = repo['metrics'][metric]
        optimal = optimal_position[i]
        print(f"  {metric}: {actual} (optimal: {optimal:.2f})")


def main():
    repo_data = load_repo_data("data/data.json")
    if not repo_data:
        print("Error: No repository data found")
        return
    
    print(f"Loaded {len(repo_data)} repositories")
    
    metrics = ['commits', 'contributors', 'open_pr', 'closed_pr', 
               'merged_pr', 'open_issue', 'closed_issue', 'stars', 'fork']
    bounds = get_min_max_metrics()
    
    print("Running Particle Swarm Optimization...")
    best_position, best_value = particle_swarm_optimization(
        dim=len(metrics), 
        bounds=bounds, 
        reward_function=reward_function,
        num_particles=50,
        max_iter=100
    )
    
    print("\nOptimal Repository Characteristics:")
    for i, metric in enumerate(metrics):
        print(f"{metric}: {best_position[i]:.2f}")
    print(f"Optimal Reward Value: {best_value:.2f}")
    
    print("\nComparing repositories to the optimal...")
    repo_scores = compare_repos_to_optimal(repo_data, best_position, bounds)
    
    repo_scores_by_reward = sorted(repo_scores, key=lambda r: r['reward'], reverse=True)
    print("\nTop 10 Repositories by Reward Value:")
    for i, repo in enumerate(repo_scores_by_reward[:10]):
        print(f"{i+1}. {repo['name']} - Reward: {repo['reward']:.2f}, Distance: {repo['distance']:.4f}")
    
    repo_scores_by_distance = sorted(repo_scores, key=lambda r: r['distance'])
    print("\nTop 10 Repositories by Proximity to Optimal:")
    for i, repo in enumerate(repo_scores_by_distance[:10]):
        print(f"{i+1}. {repo['name']} - Distance: {repo['distance']:.4f}, Reward: {repo['reward']:.2f}")

    print("\nDetailed Analysis of Best Repository:")
    print_repo_details(repo_scores_by_distance[0], best_position, metrics)


if __name__ == "__main__":
    main()
