import os
import subprocess

#command = "ls -l"
#result = subprocess.run(command, shell=True,capture_output=True,text=True)
#print(result.stdout)
#print(result.stderr) For error output

def check_root_privileges():
    if os.geteuid() != 0:
        print("This program requires root privileges. Please run it as a root user.")
        exit(1)

# Call the function to check for root privileges
check_root_privileges()