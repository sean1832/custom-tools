import os
import sys
import argparse

class PythonProjectInstaller:
    """
    A class to automate the installation of Python projects from GitHub.
    It handles cloning the repository, creating a virtual environment,
    and installing the necessary requirements and setup.
    """
    def __init__(self, url):
        """
        Initializes the PythonProjectInstaller with the given GitHub repository URL.
        Also, initializes the source directory where the repository will be cloned.
        """
        self.url = url
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.code_dir = os.path.join(self.parent_dir, 'code')
        self.repo_name = self.url.split("/")[-1].replace(".git", "")
        self.local_dir = os.path.join(self.code_dir, self.repo_name, 'local')
        self._create_code_dir()
        
    def _create_code_dir(self):
        """
        Creates the source directory if it does not exist.
        """
        if not os.path.isdir(self.code_dir):
            os.mkdir(self.code_dir)
            print('code directory created')
    
    def is_python_project(self, repo_dir):
        """
        Determines whether the given repository directory is a Python project.
        """
        python_indicators = ['requirements.txt', 'setup.py']
        for root, dirs, files in os.walk(repo_dir):
            if any(file.endswith('.py') or file in python_indicators for file in files):
                return True
        return False
    
    def clone_repo(self):
        """
        Clones the repository from the given URL to the source directory.
        """
        os.chdir(self.code_dir)
        
        repo_dir = os.path.join(self.code_dir, self.repo_name)
        
        if os.path.isdir(repo_dir):
            print(f"Repository {self.repo_name} already exists locally.")
            return repo_dir
        
        if self._user_confirmation('Repo does not exist locally. Do you want to clone it? (y/n)'):
            os.system(f'git clone {self.url}')
            print('Repository cloned')
            return repo_dir
        else:
            self._abort_installation('Repository not cloned')
    
    def create_venv(self, repo_dir):
        """
        Creates a virtual environment in the given repository directory.
        """
        venv_dir = os.path.join(repo_dir, 'venv')
        if os.path.isdir(venv_dir):
            print('Virtual environment already exists.')
            return venv_dir
        
        if self._user_confirmation('Virtual environment does not exist locally. Do you want to create it? (y/n)'):
            os.system(f'python -m venv {venv_dir}')
            print(f'Virtual environment created at {venv_dir}.')
            return venv_dir
        else:
            self._abort_installation('Virtual environment not created')
    
    def install_requirements_and_setup(self, repo_dir, venv_dir):
        """
        Installs the requirements and setup from the requirements.txt and setup.py files
        located in the given repository directory, using the specified virtual environment.
        """
        activate_script = os.path.join(venv_dir, 'Scripts', 'activate')
        if not os.path.isfile(activate_script):
            self._abort_installation(f"Error: {activate_script} not found.")
        
        requirements_file = os.path.join(repo_dir, 'requirements.txt')
        install_requirements_cmd = ""
        if os.path.isfile(requirements_file) and self._user_confirmation('Requirements.txt found. Do you want to install? (y/n)'):
            install_requirements_cmd = f' && {os.path.join(venv_dir, "Scripts", "pip")} install -r {requirements_file}'
            self.create_stamp(repo_dir, 'installed')
            print('Requirements installed')
        
        setup_file = os.path.join(repo_dir, 'setup.py')
        install_setup_cmd = ""
        if os.path.isfile(setup_file) and self._user_confirmation('setup.py found. Do you want to install? (y/n)'):
            # Changing to the repository directory before running pip install .
            install_setup_cmd = f' && cd {repo_dir} && {os.path.join(venv_dir, "Scripts", "pip")} install .'
            self.create_stamp(repo_dir, 'installed')
            print('Setup installed')
        
        os.system(f'{activate_script}{install_requirements_cmd}{install_setup_cmd}')


    
    def create_stamp(self, repo_dir, content, stamp_file='install_status'):
        """
        Creates a stamp file in the given repository directory with the specified content.
        """
        if not os.path.isdir(self.local_dir):
            os.mkdir(self.local_dir)
        
        stamp_file_path = os.path.join(repo_dir, self.local_dir, stamp_file)
        with open(stamp_file_path, 'w') as f:
            f.write(content)
        print(f'{stamp_file} file created')
    
    def _user_confirmation(self, message):
        """
        Prompts the user for confirmation with the given message and returns True if the user confirms.
        """
        result = input(message)
        return result.lower() == 'y'
    
    def _abort_installation(self, message):
        """
        Aborts the installation process and exits the program with the given message.
        """
        print(message)
        print('Installation aborted')
        sys.exit()
    
    def install(self):
        """
        Orchestrates the installation process including cloning the repo, creating a virtual environment,
        and installing the requirements and setup.
        """
        try:
            repo_dir = self.clone_repo()
            if not repo_dir or not self.is_python_project(repo_dir):
                self._abort_installation(f"The repository at {self.url} does not appear to be a Python project.")
            
            venv_dir = self.create_venv(repo_dir)
            if not venv_dir:
                self._abort_installation(f"Error: Failed to create virtual environment in {repo_dir}")
            
            stamp_file = os.path.join(self.local_dir, 'install_status')
            if os.path.isfile(stamp_file):
                with open(stamp_file, 'r') as f:
                    content = f.read()
                if content == 'installed':
                    print('Requirements already installed. Skipping...')
                    return
            self.install_requirements_and_setup(repo_dir, venv_dir)
            # print('Installation complete.')
        except Exception as e:
            print(f"Error: {e}")
            print('Installation Failed.')

def main():
    """
    The main function that parses the command-line arguments and initiates the installation process.
    """
    description = 'Install Python project from GitHub. The project will be cloned to the code directory under the parent directory of this script.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('url', type=str, help='URL of the GitHub repository')
    args = parser.parse_args()
    installer = PythonProjectInstaller(args.url)
    installer.install()

if __name__ == '__main__':
    main()
