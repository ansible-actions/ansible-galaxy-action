import subprocess
import os

# Specify the name of the environment variable you want to read
env_var_name = "TEST"

# Attempt to read the environment variable
env_var_value = os.getenv(env_var_name)

# Check if the environment variable exists
if env_var_value is not None:
    print(f"The value of {env_var_name} is: {env_var_value}")
else:
    print(f"The environment variable {env_var_name} is not set.")


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
