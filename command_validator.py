def validate_command(command):
    # Define allowed commands
    allowed_commands = ["execute_command", "view_swarm_status", "request_work"]
    
    # Check if the command is allowed
    if command in allowed_commands:
        return True
    
    return False