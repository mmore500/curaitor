import os
import yaml

# Get root directory path
root_dir = os.path.dirname(os.path.dirname(__file__))
file_path = f"{root_dir}/prompts.yml"

def read_prompts(file_path: str) -> dict:
    """
    Read prompts from a YAML file.

    Args:
        file_path: Path to the YAML file

    Returns:
        dict: Prompts from the YAML file
    """
    with open(file_path, "r") as file:
        prompts = yaml.safe_load(file)
    return prompts

def choose_prompt(prompts: dict) -> str:
    """
    Allow user to choose a prompt from the given dictionary.

    Args:
        prompts: Dictionary of prompts

    Returns:
        str: Selected prompt
    """
    print("Please choose one of the following options:")
    keys = list(prompts.keys())
    print(f"Here are the choices currently supported: {keys}")

    while True:
        choice = input("Enter the name of your choice: ")
        if choice in keys:
            print(f"You selected prompt: {choice}")
            return prompts[choice]
        print("Please enter a valid choice.")

# Example usage
# selected_key = choose_prompt(prompts=read_prompts(file_path))
# print(selected_key)