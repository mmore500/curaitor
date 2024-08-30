import os
import subprocess

# Define output folder as current script directory
output_folder = os.path.dirname(__file__)

# OSF project details
project_id = "4udrf"  # Replace with actual project ID
username = "lizhenzhupearl@gmail.com"

# Construct OSF clone command
command = f"osf -p {project_id} -u {username} clone {output_folder}"

# Execute command and capture output
process = subprocess.Popen(
   command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
)
stdout, stderr = process.communicate()

# Decode and print output
print("Output:", stdout.decode("utf-8"))

if stderr:
   print("Errors:", stderr.decode("utf-8"))