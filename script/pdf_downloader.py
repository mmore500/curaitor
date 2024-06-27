import subprocess
import os

# Define the output folder
output_folder = os.path.dirname(__file__)
project_id = (
    "4udrf"  # Replace with your actual project ID; need to set the token
)
username = "lizhenzhupearl@gmail.com"

# Construct the command with the output folder
command = f"osf -p {project_id} -u {username} clone {output_folder}"


# Running the command
process = subprocess.Popen(
    command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
)

# Capture the output and errors
stdout, stderr = process.communicate()

# Decode the output and errors (assuming they are in bytes)
stdout = stdout.decode("utf-8")
stderr = stderr.decode("utf-8")

# Print the output and errors
print("Output:")
print(stdout)

if stderr:
    print("Errors:")
    print(stderr)
