import subprocess

# Command to run
command = ["ansible", "--version"]

# Run the command
try:
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    # Print the output
    print("Ansible Version Information:")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("Error running Ansible command:", e)
