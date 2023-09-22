import json
import argparse
import toml

def read_json(json_file, info=None):
    with open(json_file, 'r') as f:
        data = json.load(f)
    if info:
        return data.get(info, "Info not found in JSON")
    else:
        return data

def read_toml(toml_file, info=None):
    try:
        data = toml.load(toml_file)
        if info:
            return data.get(info, "Info not found in TOML")
        else:
            return data
    except toml.TomlDecodeError as e:
        print(f"Error: {toml_file} is not a valid TOML file")
        print(f"Details: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Utility to get information from various file formats in this project')
    
    parser.add_argument('--file', required=True, help='File to read')
    parser.add_argument('--info', help='Specific information to retrieve from the file')
    parser.add_argument('--format', choices=['json', 'toml'], default='json', help='Format of the file to read')
    
    args = parser.parse_args()
    
    try:
        if args.format == 'json':
            data = read_json(args.file, args.info)
        elif args.format == 'toml':
            data = read_toml(args.file, args.info)
        else:
            raise ValueError(f"Unsupported format: {args.format}")
        
        print(data)
    except FileNotFoundError:
        print(f"Error: File {args.file} not found")
    except json.JSONDecodeError:
        print(f"Error: {args.file} is not a valid JSON file")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()


