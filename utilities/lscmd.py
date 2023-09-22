import os
import argparse

def list_files(directory):
    try:
        # Get all files and subdirectories in the directory
        entries = os.listdir(directory)

        # Filter out subdirectories and only keep files
        files_only = [entry for entry in entries if os.path.isfile(os.path.join(directory, entry))]

        outputs = []
        for file in files_only:
            if file.endswith('.bat'):
                splited = file.split('.')
                file = splited[0]
                outputs.append(file)

        return outputs

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
def main():
    parser = argparse.ArgumentParser(description='List custom commands')
    parser.add_argument('-d', '--directory', type=str, help='Directory to list the files from')
    args = parser.parse_args()

    files = list_files(args.directory)
    print("Custom commands:\n")
    print("====================================\n")
    for file in files:
        print(file)
    print("\n====================================")

if __name__ == '__main__':
    main()
