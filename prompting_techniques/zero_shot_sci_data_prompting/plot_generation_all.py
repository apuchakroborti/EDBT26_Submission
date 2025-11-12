import os
import subprocess

# Specify the directory containing the Python files
directory = '/Users/apukumarchakroborti/gsu_research/llam_test/prompting_techniques/graph_generation_with_label_mapping'

# Get a list of all Python files in the directory
python_files = [f for f in os.listdir(directory) if f.endswith('.py')]

# Execute each Python file one by one
for file in python_files:
    file_path = os.path.join(directory, file)
    print(f"Executing {file_path}...")
    subprocess.run(['python', file_path])  # Use 'python3' instead of 'python' if necessary
