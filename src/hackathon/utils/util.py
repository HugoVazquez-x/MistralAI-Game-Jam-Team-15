import yaml

def read_yaml(file_path):
    """
    Reads a YAML file and returns its contents as a Python object.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict or list: The parsed YAML structure (dictionary or list).
    """
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
