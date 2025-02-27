import requests
import json
import time
import csv
from datetime import datetime

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
    
    # Add your personal token for higher rate limits (optional)
    # headers["Authorization"] = "token YOUR_GITHUB_TOKEN"
    
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

def collect_top_repos(total_repos=1000):
    """Collect top repositories data"""
    all_repos = []
    per_page = 100  # Max allowed by GitHub API
    total_pages = (total_repos + per_page - 1) // per_page  # Ceiling division
    
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
    
    return all_repos[:total_repos]  # Ensure we don't exceed the requested count

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
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Data saved to {filename}")

def save_to_csv(data, filename='top_github_repos.csv'):
    """Save repositories data to CSV file"""
    if not data:
        print("No data to save")
        return
        
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

def run_collection(total_repos=1000):
    """Main function to run the collection process"""
    start_time = time.time()
    print(f"Starting collection of top {total_repos} GitHub repositories...")
    
    # Collect raw repository data
    repos = collect_top_repos(total_repos)
    
    if not repos:
        print("No repositories collected.")
        return
    
    # Extract and process repository data
    processed_repos = [extract_repo_data(repo) for repo in repos]
    
    # Save data in multiple formats
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_to_json(processed_repos, f"../db/top_github_repos_{timestamp}.json")
    save_to_csv(processed_repos, f"../db/top_github_repos_{timestamp}.csv")
    
    elapsed_time = time.time() - start_time
    print(f"Collection complete: {len(processed_repos)} repositories collected in {elapsed_time:.2f} seconds.")
    return processed_repos

if __name__ == "__main__":
    run_collection(1000)
