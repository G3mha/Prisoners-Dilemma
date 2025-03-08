import requests
import json
import time
import csv
from datetime import datetime
import os
import argparse
import re

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
    
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "GitHub-Repo-Metrics-Collector"
    }
    
    if 'GITHUB_TOKEN' in globals() and GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403 and 'rate limit exceeded' in response.text:
        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        current_time = int(time.time())
        sleep_time = reset_time - current_time + 5
        
        print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)
        return fetch_top_repos(page, per_page)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def handle_rate_limit(response):
    """Handle GitHub API rate limiting"""
    reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
    current_time = int(time.time())
    sleep_time = reset_time - current_time + 5
    
    print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds.")
    time.sleep(sleep_time)

def get_last_page_number(response):
    """Extract the last page number from the Link header"""
    try:
        if 'Link' in response.headers and 'rel="last"' in response.headers['Link']:
            link_header = response.headers['Link']
            link_parts = link_header.split(',')
            
            for part in link_parts:
                if 'rel="last"' in part:
                    url_part = part.split(';')[0].strip('<>')
                    
                    # Use regex to find the page parameter
                    match = re.search(r'[&?]page=(\d+)', url_part)
                    if match:
                        page_num = int(match.group(1))
                        return page_num
            
            if "page=" in link_header:
                parts = link_header.split("page=")
                for part in parts[1:]:  # Skip the first part before "page="
                    num_str = ""
                    for char in part:
                        if char.isdigit():
                            num_str += char
                        elif num_str:  # Stop at the first non-digit after finding digits
                            break
                    if num_str:
                        page_num = int(num_str)
                        return page_num
        
        # If we get here, there's no pagination or we couldn't extract the page number
        return 1
    except Exception as e:
        return 1

def fetch_commit_count(repo_full_name, headers):
    """Fetch total commit count for a repository"""
    url = f"https://api.github.com/repos/{repo_full_name}/commits"
    params = {"per_page": 1}
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        last_page = get_last_page_number(response)
        # GitHub API paginates with 30 items per page by default when per_page is not specified
        # But we specified per_page=1, so each page has 1 commit
        return last_page
    elif response.status_code == 403 and 'rate limit exceeded' in response.text:
        handle_rate_limit(response)
        return fetch_commit_count(repo_full_name, headers)
    else:
        print(f"Error fetching commit count for {repo_full_name}: {response.status_code}")
        return 0

def fetch_contributors_count(repo_full_name, headers):
    """Fetch contributor count for a repository"""
    url = f"https://api.github.com/repos/{repo_full_name}/contributors"
    params = {"per_page": 1}  # Removed anon=1 which was causing parsing issues
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        last_page = get_last_page_number(response)
        return last_page
    elif response.status_code == 403 and 'rate limit exceeded' in response.text:
        handle_rate_limit(response)
        return fetch_contributors_count(repo_full_name, headers)
    else:
        print(f"Error fetching contributor count for {repo_full_name}: {response.status_code}")
        return 0

def fetch_pull_requests_counts(repo_full_name, headers):
    """Fetch pull request counts (open, closed, merged) for a repository"""
    counts = {
        "open_pr": 0,
        "closed_pr": 0,
        "merged_pr": 0
    }
    
    # Fetch open PRs
    url = f"https://api.github.com/repos/{repo_full_name}/pulls"
    params = {"state": "open", "per_page": 1}
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        counts["open_pr"] = get_last_page_number(response)
    elif response.status_code == 403 and 'rate limit exceeded' in response.text:
        handle_rate_limit(response)
        return fetch_pull_requests_counts(repo_full_name, headers)
    
    # Fetch closed PRs
    url = f"https://api.github.com/repos/{repo_full_name}/pulls"
    params = {"state": "closed", "per_page": 1}
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        counts["closed_pr"] = get_last_page_number(response)
    
    # Merged PRs requires individual checking, use sample to estimate
    # For large repos, get a reasonable estimation by sampling
    url = f"https://api.github.com/repos/{repo_full_name}/pulls"
    params = {"state": "closed", "per_page": 20}  # Sample 20 closed PRs
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        closed_prs = response.json()
        merged_count = 0
        for pr in closed_prs:
            if pr.get('merged_at'):
                merged_count += 1
        
        # Calculate the ratio of merged to closed from sample
        if closed_prs:
            merge_ratio = merged_count / len(closed_prs)
            counts["merged_pr"] = int(counts["closed_pr"] * merge_ratio)
        
    return counts

def fetch_issues_counts(repo_full_name, headers):
    """Fetch issue counts (open, closed) for a repository"""
    counts = {
        "open_issue": 0,
        "closed_issue": 0
    }
    
    # Fetch open issues
    url = f"https://api.github.com/repos/{repo_full_name}/issues"
    params = {"state": "open", "per_page": 1}
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        counts["open_issue"] = get_last_page_number(response)
    elif response.status_code == 403 and 'rate limit exceeded' in response.text:
        handle_rate_limit(response)
        return fetch_issues_counts(repo_full_name, headers)
    
    # Fetch closed issues
    url = f"https://api.github.com/repos/{repo_full_name}/issues"
    params = {"state": "closed", "per_page": 1}
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        counts["closed_issue"] = get_last_page_number(response)
    
    return counts

def collect_repo_metrics(repo, headers):
    """Collect specific repository metrics"""
    repo_full_name = repo["full_name"]
    print(f"Collecting metrics for {repo_full_name}...")
    
    # Extract basic repo data
    basic_data = {
        "name": repo["name"],
        "full_name": repo["full_name"],
        "owner": repo["owner"]["login"],
        "description": repo["description"],
        "language": repo["language"],
        "stars": repo["stargazers_count"],
        "fork": repo["forks_count"],
        "created_at": repo["created_at"],
        "updated_at": repo["updated_at"]
    }
    
    # Get commit count
    basic_data["commits"] = fetch_commit_count(repo_full_name, headers)
    
    # Get contributor count
    basic_data["contributors"] = fetch_contributors_count(repo_full_name, headers)
    
    # Get pull request counts
    pr_counts = fetch_pull_requests_counts(repo_full_name, headers)
    basic_data.update(pr_counts)
    
    # Get issue counts
    issue_counts = fetch_issues_counts(repo_full_name, headers)
    basic_data.update(issue_counts)
    
    return basic_data

def save_to_json(data, filename='data/data.json'):
    """Save repositories data to JSON file"""
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)
        
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Data saved to {filename}")

def save_to_csv(data, filename='data/data.csv'):
    """Save repositories data to CSV file"""
    if not data:
        print("No data to save")
        return
    
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)
        
    fieldnames = sorted(list(data[0].keys()))
    
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data saved to {filename}")

def collect_data(total_repos=20):
    """Main function to collect repository metrics"""
    start_time = time.time()
    
    print(f"Starting collection of top {total_repos} GitHub repositories...")
    
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "GitHub-Repo-Metrics-Collector"
    }
    
    if 'GITHUB_TOKEN' in globals() and GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
        print("Using GitHub token for authentication")
    else:
        print("WARNING: No GitHub token provided. API rate limits will be very restrictive.")
    
    all_repos = []
    per_page = 100
    total_pages = (total_repos + per_page - 1) // per_page
    
    for page in range(1, total_pages + 1):
        print(f"Fetching page {page}/{total_pages}...")
        
        response_data = fetch_top_repos(page, per_page)
        if not response_data:
            break
            
        repos = response_data.get('items', [])
        all_repos.extend(repos)
        
        if len(repos) < per_page:
            break
            
        time.sleep(2)
    
    all_repos = all_repos[:total_repos]
    
    # Process each repository
    processed_repos = []
    for i, repo in enumerate(all_repos):
        try:
            print(f"Processing repository {i+1}/{len(all_repos)}: {repo['full_name']}")
            repo_metrics = collect_repo_metrics(repo, headers)
            processed_repos.append(repo_metrics)
            print(f"Successfully processed {repo['full_name']}")
            
            # Be extra cautious with rate limits between repositories
            time.sleep(2)
        except Exception as e:
            print(f"Error processing repository {repo['full_name']}: {str(e)}")
            continue
    
    # Save data in multiple formats
    save_to_json(processed_repos)
    save_to_csv(processed_repos)
    
    elapsed_time = time.time() - start_time
    print(f"Collection complete: {len(processed_repos)}/{total_repos} repositories collected in {elapsed_time:.2f} seconds.")
    return processed_repos

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Collect GitHub repository metrics for PSO analysis')
    parser.add_argument('--repos', type=int, default=20, help='Number of repositories to collect (default: 20)')
    parser.add_argument('--token', type=str, help='GitHub personal access token')
    
    args = parser.parse_args()
    
    if args.token:
        GITHUB_TOKEN = args.token
    
    collect_data(total_repos=args.repos)
