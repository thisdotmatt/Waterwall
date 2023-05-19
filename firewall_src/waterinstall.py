import os
import subprocess

def check_root_privileges():
    if os.geteuid() != 0:
        print("This program requires root privileges. Please run it as a root user.")
        exit(1)

# Call the function to check for root privileges
check_root_privileges()

command = "test -f /usr/bin/waterwall && echo \"$FILE exists.\""
result = subprocess.run(command, shell=True,capture_output=True,text=True)
if result != "/usr/bin/waterwall exists.":
    print("Program not installed")
    exit(1)

command = "sudo mv /usr/bin/waterwall /etc/systemd/system/"
subprocess.run(command, shell=True)
command = "sudo systemctl start waterwall"
subprocess.run(command, shell=True)

#Stop Waterwall (why would you ever do this)
# command = "sudo systemctl stop waterwall"
# subprocess.run(command, shell=True)