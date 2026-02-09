import subprocess

def execute_command(command, ip_address):
    # Execute the command on the remote machine
    subprocess.run(["ssh", ip_address, command])