import os
import argparse

# get parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# check if src directory exists
src_dir = os.path.join(parent_dir, 'src')
if not os.path.isdir(src_dir):
    os.mkdir(src_dir)
    print('src directory created')

def is_python_project(repo_dir):
    python_indicators = ['requirements.txt', 'setup.py']
    for root, dirs, files in os.walk(repo_dir):
        for file in files:
            if file.endswith('.py') or file in python_indicators:
                return True
    return False

def clone_repo(url):
    try:
        # change to src directory
        os.chdir(src_dir)
        
        # get the name of the repository
        repo_name = url.split("/")[-1].replace(".git", "")
        repo_dir = os.path.join(src_dir, repo_name)
        
        # check if the repository already exists locally
        if os.path.isdir(repo_dir):
            print(f"Repository {repo_name} already exists locally.")
            return repo_dir
        
        # clone repository
        os.system(f'git clone {url}')
        print('repository cloned')
        
        return repo_dir
    except Exception as e:
        print(f"Error cloning repository '{url}': {e}")
        return None

def create_venv(repo_dir):
    try:
        # create virtual environment inside the cloned repository
        venv_dir = os.path.join(repo_dir, 'venv')
        
        # check if the virtual environment already exists
        if os.path.isdir(venv_dir):
            print('Virtual environment already exists.')
            return venv_dir
        
        os.system(f'python -m venv {venv_dir}')
        print('Virtual environment created.')
        
        return venv_dir
    except Exception as e:
        print(f"Error creating virtual environment: {e}")
        return None

def install_requirements(repo_dir, venv_dir):
    try:
        # activate virtual environment and install requirements
        requirements_file = os.path.join(repo_dir, 'requirements.txt')
        if os.path.isfile(requirements_file):
            os.system(f'{os.path.join(venv_dir, "bin", "pip")} '
                      f'install -r {requirements_file}')
            print('requirements installed.')
            create_stamp(repo_dir, 'installed')
        else:
            print('requirements.txt not found.')
            create_stamp(repo_dir, 'not found')
    except Exception as e:
        print(f"Error installing requirements: {e}")

def create_stamp(repo_dir, content, stamp_file='install_status'):
    try:
        # create stamp file
        stamp_file = os.path.join(repo_dir, stamp_file)
        with open(stamp_file, 'w') as f:
            f.write(content)
        print('{stamp_file} file created')
    except Exception as e:
        print(f"Error creating {stamp_file} file: {e}")

# main installation function

def install(url):
    repo_dir = clone_repo(url)
    if not repo_dir:
        print(f"Error: Failed to clone repository from {url}")
        return
    
    if not is_python_project(repo_dir):
        print(f"The repository at {url} does not appear to be a Python project.")
        return
    
    venv_dir = create_venv(repo_dir)
    if not venv_dir:
        print(f"Error: Failed to create virtual environment in {repo_dir}")
        return
    
    # check if requirements have already been installed
    stamp_file = os.path.join(repo_dir, 'install_status')
    if os.path.isfile(stamp_file):
        with open(stamp_file, 'r') as f:
            content = f.read()
        if content == 'installed':
            print('requirements already installed. Skipping...')
            return
        elif content == 'not found':
            # check if requirements.txt exists
            requirements_file = os.path.join(repo_dir, 'requirements.txt')
            if os.path.isfile(requirements_file):
                install_requirements(repo_dir, venv_dir)
            else:
                print('requirements.txt not exist. Skipping...')
        else:
            install_requirements(repo_dir, venv_dir)


def main():
    parser = argparse.ArgumentParser(description='Install Python project from GitHub')
    parser.add_argument('url', type=str, help='URL of the GitHub repository')
    args = parser.parse_args()
    install(args.url)