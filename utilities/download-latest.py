import requests
import argparse
import os
import zipfile

def download_file(file_url, output_directory):
    file_name = os.path.join(output_directory, file_url.split('/')[-1])
    try:
        with requests.get(file_url, stream=True) as response:
            response.raise_for_status()  # Check if the request was successful
            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        print(f"File has been downloaded to {file_name}.")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return 1, None
    return 0, file_name


def extract_zip(file_path, output_directory):
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(output_directory)
        print(f"Files have been extracted to {output_directory}")
    except zipfile.BadZipFile as e:
        print(f"Error occurred: {e}")
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(description="Download and extract a zip file from a direct link.")
    parser.add_argument("url", help="Direct link to the zip file.")
    parser.add_argument("--output", default=".", help="Output directory to save and extract the file. Defaults to current directory.")
    
    args = parser.parse_args()
    
    exit_code, file_path = download_file(args.url, args.output)
    if exit_code == 0 and file_path:
        exit_code = extract_zip(file_path, args.output)
    exit(exit_code)

if __name__ == "__main__":
    main()
