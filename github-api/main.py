import requests
import json
import time
import csv
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
import math
import os
import argparse

def fetch_top_repos(page=1, per_page=100):
    """Fetch top repositories sorted by stars from GitHub API"""
    url = f"https://api.github.com/search/repositories"
    params = {
        "q": "stars:>1",
        "sort": "stars",
        "order": "desc",
        "page": page,
        "per_page": per_page
    }
    
    # GitHub requires a User-Agent header
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "GitHub-Top-Repos-Collector"
    }
    
    # Add personal token if provided via command line
    if 'GITHUB_TOKEN' in globals() and GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403 and 'rate limit exceeded' in response.text:
        # Handle rate limiting
        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        current_time = int(time.time())
        sleep_time = reset_time - current_time + 5  # Add 5 seconds buffer
        
        print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)
        return fetch_top_repos(page, per_page)  # Retry after sleeping
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def fetch_contributors(repo_full_name, headers):
    """Fetch contributor statistics for a repository"""
    url = f"https://api.github.com/repos/{repo_full_name}/contributors"
    params = {"per_page": 100}
    
    contributors = []
    page = 1
    
    while True:
        params["page"] = page
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            page_contributors = response.json()
            if not page_contributors:
                break
            contributors.extend(page_contributors)
            page += 1
            
            # Check if we've reached the last page
            if len(page_contributors) < 100:
                break
                
            # Respect rate limits
            time.sleep(0.5)
        elif response.status_code == 403 and 'rate limit exceeded' in response.text:
            handle_rate_limit(response)
        else:
            print(f"Error fetching contributors for {repo_full_name}: {response.status_code}")
            break
    
    return contributors

def fetch_commit_frequency(repo_full_name, headers):
    """Fetch commit statistics for a repository over the past year"""
    url = f"https://api.github.com/repos/{repo_full_name}/stats/commit_activity"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 202:
        # GitHub is computing the statistics, retry after a short delay
        print(f"GitHub is computing stats for {repo_full_name}, waiting...")
        time.sleep(5)
        return fetch_commit_frequency(repo_full_name, headers)
    elif response.status_code == 403 and 'rate limit exceeded' in response.text:
        handle_rate_limit(response)
        return fetch_commit_frequency(repo_full_name, headers)
    else:
        print(f"Error fetching commit frequency for {repo_full_name}: {response.status_code}")
        return []

def handle_rate_limit(response):
    """Handle GitHub API rate limiting"""
    reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
    current_time = int(time.time())
    sleep_time = reset_time - current_time + 5  # Add 5 seconds buffer
    
    print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds.")
    time.sleep(sleep_time)

def calculate_contribution_metrics(repo_full_name, headers):
    """Calculate only essential contribution metrics to stay within API rate limits"""
    metrics = {}
    
    # 1. Number of unique contributors
    contributors = fetch_contributors(repo_full_name, headers)
    metrics["unique_contributors_count"] = len(contributors)
    
    # Calculate distribution of contributions
    if contributors:
        contribution_counts = [c.get("contributions", 0) for c in contributors]
        metrics["median_contributions_per_contributor"] = statistics.median(contribution_counts) if contribution_counts else 0
        metrics["mean_contributions_per_contributor"] = statistics.mean(contribution_counts) if contribution_counts else 0
        
        # Calculate Gini coefficient for contribution inequality
        sorted_contributions = sorted(contribution_counts)
        cumsum = [0]
        for i, x in enumerate(sorted_contributions):
            cumsum.append(cumsum[i] + x)
        n = len(sorted_contributions)
        if n > 0 and cumsum[-1] > 0:
            metrics["contribution_gini_coefficient"] = (2 * sum(i * y for i, y in enumerate(sorted_contributions, 1)) / 
                                               (n * cumsum[-1])) - (n + 1) / n
        else:
            metrics["contribution_gini_coefficient"] = 0
    
    # 2. Commit frequency
    commit_stats = fetch_commit_frequency(repo_full_name, headers)
    if commit_stats:
        weekly_commits = [week.get("total", 0) for week in commit_stats]
        metrics["total_annual_commits"] = sum(weekly_commits)
        metrics["average_weekly_commits"] = statistics.mean(weekly_commits) if weekly_commits else 0
        metrics["commit_consistency"] = statistics.stdev(weekly_commits) / max(metrics["average_weekly_commits"], 1) if weekly_commits and len(weekly_commits) > 1 else 0
    
    return metrics

def collect_enhanced_repo_data(repo, headers):
    """Collect enhanced repository data including contribution metrics"""
    repo_full_name = repo["full_name"]
    print(f"Collecting enhanced data for {repo_full_name}...")
    
    # Get basic repo data
    basic_data = extract_repo_data(repo)
    
    # Get advanced contribution metrics
    try:
        contribution_metrics = calculate_contribution_metrics(repo_full_name, headers)
        return {**basic_data, **contribution_metrics}
    except Exception as e:
        print(f"Error collecting enhanced data for {repo_full_name}: {str(e)}")
        return basic_data

def extract_repo_data(repo):
    """Extract relevant data from a repository object"""
    return {
        "name": repo["name"],
        "full_name": repo["full_name"],
        "owner": repo["owner"]["login"],
        "owner_type": repo["owner"]["type"],
        "html_url": repo["html_url"],
        "description": repo["description"],
        "stars": repo["stargazers_count"],
        "forks": repo["forks_count"],
        "watchers": repo["watchers_count"],
        "language": repo["language"],
        "open_issues": repo["open_issues_count"],
        "created_at": repo["created_at"],
        "updated_at": repo["updated_at"],
        "pushed_at": repo["pushed_at"],
        "size": repo["size"],
        "license": repo["license"]["name"] if repo["license"] else None,
        "topics": repo.get("topics", []),
        "default_branch": repo["default_branch"],
        "has_wiki": repo["has_wiki"],
        "has_pages": repo["has_pages"],
        "archived": repo["archived"],
        "disabled": repo["disabled"]
    }

def save_to_json(data, filename='top_github_repos.json'):
    """Save repositories data to JSON file"""
    # Ensure directory exists
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)
        
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Data saved to {filename}")

def save_to_csv(data, filename='top_github_repos.csv'):
    """Save repositories data to CSV file"""
    if not data:
        print("No data to save")
        return
    
    # Ensure directory exists
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)
        
    # Get all unique keys from all repositories
    fieldnames = set()
    for repo in data:
        fieldnames.update(repo.keys())
    fieldnames = sorted(list(fieldnames))
    
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data saved to {filename}")

def save_checkpoint(processed_repos, current_index, total_repos, timestamp):
    """Save a checkpoint of processed repositories"""
    checkpoint_dir = "../db"
    
    # Ensure the directory exists
    os.makedirs(checkpoint_dir, exist_ok=True)
    
    checkpoint_file = f"{checkpoint_dir}/github_checkpoint_{timestamp}.json"
    
    checkpoint_data = {
        "timestamp": datetime.now().isoformat(),
        "processed_count": len(processed_repos),
        "current_index": current_index,
        "total_repos": total_repos,
        "repos": processed_repos
    }
    
    with open(checkpoint_file, 'w', encoding='utf-8') as f:
        json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)
    
    print(f"Checkpoint saved: {len(processed_repos)}/{total_repos} repositories processed")
    
def load_checkpoint(timestamp=None):
    """Load the most recent checkpoint or a specific checkpoint"""
    checkpoint_dir = "../db"
    
    # Ensure the directory exists
    os.makedirs(checkpoint_dir, exist_ok=True)
    
    # Get all checkpoint files
    checkpoint_files = [f for f in os.listdir(checkpoint_dir) if f.startswith("github_checkpoint_") and f.endswith(".json")]
    
    if not checkpoint_files:
        print("No checkpoints found")
        return [], 0, 0, None
    
    # If timestamp is provided, try to find that specific checkpoint
    if timestamp:
        target_file = f"github_checkpoint_{timestamp}.json"
        if target_file in checkpoint_files:
            checkpoint_file = os.path.join(checkpoint_dir, target_file)
        else:
            print(f"Checkpoint for timestamp {timestamp} not found")
            return [], 0, 0, None
    else:
        # Otherwise, get the most recent checkpoint
        checkpoint_files.sort(reverse=True)
        checkpoint_file = os.path.join(checkpoint_dir, checkpoint_files[0])
        
    try:
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            checkpoint_data = json.load(f)
            
        processed_repos = checkpoint_data.get("repos", [])
        current_index = checkpoint_data.get("current_index", 0)
        total_repos = checkpoint_data.get("total_repos", 0)
        timestamp = checkpoint_file.split("_")[-1].split(".")[0]
        
        print(f"Checkpoint loaded: {len(processed_repos)}/{total_repos} repositories already processed")
        return processed_repos, current_index, total_repos, timestamp
    
    except Exception as e:
        print(f"Error loading checkpoint: {str(e)}")
        return [], 0, 0, None

def run_enhanced_collection(total_repos=20, resume_from_checkpoint=False):  # Reduced default to 20 due to API limits
    """Main function to run the enhanced collection process with checkpoint support"""
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Try to load checkpoint if requested
    processed_repos = []
    current_index = 0
    if resume_from_checkpoint:
        processed_repos, current_index, saved_total, saved_timestamp = load_checkpoint()
        if processed_repos and current_index < saved_total:
            print(f"Resuming collection from checkpoint at index {current_index}")
            timestamp = saved_timestamp or timestamp
            
            # If we're resuming, use the same total as before unless explicitly changed
            if total_repos == 20:  # The default value
                total_repos = saved_total
    
    print(f"Starting enhanced collection of top {total_repos} GitHub repositories...")
    
    # GitHub requires a User-Agent header
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "GitHub-Top-Repos-Collector"
    }
    
    # Add GitHub token if available
    if 'GITHUB_TOKEN' in globals() and GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
        print("Using GitHub token for authentication")
    else:
        print("WARNING: No GitHub token provided. API rate limits will be very restrictive.")
    
    # Only fetch repositories if we need more
    all_repos = []
    if len(processed_repos) < total_repos:
        # Calculate how many more repos we need
        remaining_repos = total_repos - len(processed_repos)
        
        per_page = 100  # Max allowed by GitHub API
        total_pages = (remaining_repos + per_page - 1) // per_page  # Ceiling division
        
        for page in range(1, total_pages + 1):
            print(f"Fetching page {page}/{total_pages}...")
            
            response_data = fetch_top_repos(page, per_page)
            if not response_data:
                break
                
            repos = response_data.get('items', [])
            all_repos.extend(repos)
            
            # Check if we've reached the end of results
            if len(repos) < per_page:
                break
                
            # Respect GitHub API rate limits
            time.sleep(2)
        
        # Ensure we don't exceed the requested count
        all_repos = all_repos[:remaining_repos]
    
    # Process each repository that hasn't been processed yet
    for i, repo in enumerate(all_repos, start=current_index):
        try:
            print(f"Processing repository {i+1}/{total_repos}: {repo['full_name']}")
            enhanced_data = collect_enhanced_repo_data(repo, headers)
            processed_repos.append(enhanced_data)
            
            # Save checkpoint after every 5 repositories or when we hit the end
            if (i + 1) % 5 == 0 or i == len(all_repos) - 1:
                save_checkpoint(processed_repos, i + 1, total_repos, timestamp)
            
            # Be extra cautious with rate limits between repositories
            time.sleep(2)
        except Exception as e:
            print(f"Error processing repository {repo['full_name']}: {str(e)}")
            # Save checkpoint on error
            save_checkpoint(processed_repos, i, total_repos, timestamp)
            # Continue with next repository
            continue
    
    # Save final data in multiple formats
    save_to_json(processed_repos, f"../db/enhanced_github_repos_{timestamp}.json")
    save_to_csv(processed_repos, f"../db/enhanced_github_repos_{timestamp}.csv")
    
    elapsed_time = time.time() - start_time
    print(f"Collection complete: {len(processed_repos)}/{total_repos} repositories collected in {elapsed_time:.2f} seconds.")
    return processed_repos

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Collect GitHub repository data with enhanced contribution metrics')
    parser.add_argument('--repos', type=int, default=20, help='Number of repositories to collect (default: 20)')
    parser.add_argument('--resume', action='store_true', help='Resume from the most recent checkpoint')
    parser.add_argument('--token', type=str, help='GitHub personal access token')
    
    args = parser.parse_args()
    
    # Add your personal token for higher rate limits (required for enhanced collection)
    if args.token:
        GITHUB_TOKEN = args.token
    
    # Collect repositories
    run_enhanced_collection(total_repos=args.repos, resume_from_checkpoint=args.resume)
