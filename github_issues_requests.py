# Import required libraries
import requests
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

def fetch_github_issues(owner="langflow-ai", repo="langflow", token=None):
    """
    Fetch issues from a GitHub repository using the GitHub REST API
    
    Args:
        owner (str): Repository owner/organization (default: "langflow-ai")
        repo (str): Repository name (default: "langflow")
        token (str, optional): GitHub personal access token for authentication
        
    Returns:
        list: List of Document objects containing issue data and metadata
    """
    # Construct the GitHub API URL for issues endpoint
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    print(f"\nInitiating GitHub issues fetch for {owner}/{repo}")
    
    # Set up request headers with proper authentication and user agent
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Python-GitHub-Issues-Example'
    }
    
    # Add authentication token if provided
    if token:
        headers['Authorization'] = f'token {token}'
        print("Using provided GitHub token for authentication")
    else:
        print("Warning: No GitHub token provided. Rate limits may apply.")
    
    try:
        print(f"Making API request to: {url}")
        # Make the GET request to GitHub API
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            issues = response.json()
            
            print(f"\nSuccessfully fetched {len(issues)} issues from {owner}/{repo}")
            print("-" * 50)
            
            docs = []
            # Process each issue and create Document objects
            for i, issue in enumerate(issues, 1):
                print(f"Processing issue {i}/{len(issues)}: {issue['title'][:50]}...")
                
                # Extract metadata from issue
                metadata = {
                    "author": issue["user"]["login"],
                    "comments": issue["comments"],
                    "body": issue["body"],
                    "labels": issue["labels"],
                    "created_at": issue["created_at"],
                }
                
                # Combine title and body for full content
                data = issue["title"]
                if issue["body"]:
                    data += issue["body"]
                
                # Create Document object and append to list
                doc = Document(page_content=data, metadata=metadata)
                docs.append(doc)
                
            print(f"\nSuccessfully processed all {len(docs)} issues into Document objects")
            return docs
                
        else:
            print(f"Failed to fetch issues. Status code: {response.status_code}")
            print(f"Error message: {response.text}")
            return []
            
    except Exception as e:
        print(f"An error occurred while fetching issues: {str(e)}")
        return []
