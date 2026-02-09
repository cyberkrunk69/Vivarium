import paramiko

def execute_command_on_own_machine(ip, command):
    # Establish a connection to the user's machine
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username='username', password='password')

    # Execute the command
    stdin, stdout, stderr = ssh.exec_command(command)

    # Close the connection
    ssh.close()