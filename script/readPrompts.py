import yaml
import os

# Path to your YAML file
root_dir = os.path.dirname(os.path.dirname(__file__))
file_path = f'{root_dir}/prompts.yml'

def read_prompts(file_path):
    """Read prompts from a YAML file."""
    with open(file_path, 'r') as file:
        prompts = yaml.safe_load(file)
    return prompts

def choose_prompt(prompts):
    # Display the keys to the user
    print("Please choose one of the following options:")
    keys = list(prompts.keys())
    print(f'Here are the choices currently support: {keys}')
    # Get user input
    while True:
        try:
            choice = input("Enter the name of your choice: ")
            if choice in keys:
                print(f"You selected prompt: {choice}")
                #print(f"Description: {prompts[choice]}")
                return prompts[choice]
            else:
                print(f"Please enter a valid choice.")
        except ValueError:
            print("Invalid input. Please enter a choice.")

# Example usage
selected_key = choose_prompt(prompts=read_prompts(file_path))
#print(selected_key)
