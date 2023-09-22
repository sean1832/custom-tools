import os
import argparse
import subprocess

# check if input is a valid git repository
def is_git_repo(repo_dir) -> bool:
    try:
        # Change to the repository directory
        os.chdir(repo_dir)
        
        # Check if the directory is a git repository
        subprocess.run(['git', 'status'], check=True)
        
        return True
    except Exception as e:
        print(f"Error checking if directory is a git repository: {e}")
        return False

def check_for_updates(repo_dir) -> bool:
    try:
        # Change to the repository directory
        os.chdir(repo_dir)
        
        # Fetch the latest changes from the remote repository
        subprocess.run(['git', 'fetch'], check=True)
        
        # Get the current tracking branch
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}'], 
                                capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error determining the tracking branch: {result.stderr.strip()}")
            return False
        
        tracking_branch = result.stdout.strip()
        
        # Check if there are any updates available
        result = subprocess.run(['git', 'rev-list', f'HEAD...{tracking_branch}', '--count'], 
                                capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error checking for updates: {result.stderr.strip()}")
            return False
        
        updates_available = int(result.stdout.strip()) > 0
        
        return updates_available
    except Exception as e:
        print(f"Error checking for updates: {e}")
        return False



def pull_updates(repo_dir):
    try:
        # Change to the repository directory
        os.chdir(repo_dir)
        
        # Pull the latest changes from the remote repository
        subprocess.run(['git', 'pull'], check=True)
        print("Repository updated successfully.")
    except Exception as e:
        print(f"Error updating repository: {e}")

def main():
    parser = argparse.ArgumentParser(description='Check for updates and pull the latest'
                                     ' changes for a git repository.')
    parser.add_argument('repo_dir', 
                        help='The local directory of the git repository to update.')
    args = parser.parse_args()

    if not is_git_repo(args.repo_dir):
        print("The specified directory is not a valid git repository.")
        return

    updates_available = check_for_updates(args.repo_dir)
    if updates_available is None:
        print("Error occurred while checking for updates.")
    elif updates_available:
        response = input("Updates are available. Pull the latest changes? (y/n) ")
        if response.lower() == 'y':
            pull_updates(args.repo_dir)
        elif response.lower() == 'n':
            print("Repository not updated.")
        else:
            print("Invalid response. Repository not updated.")
    else:
        print("Repository is up to date.")


if __name__ == '__main__':
    main()
