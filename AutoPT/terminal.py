import subprocess
import time

class InteractiveShell:
    def __init__(self, timeout=30):
        # Set timeout for command execution
        self.timeout = timeout

    def execute_command(self, command: str):
        """
        Execute a command locally on the machine.
        """
        # Clean the command
        command = command.strip()

        # Handle unsupported commands
        if 'nano ' in command:
            return "nano is not supported in this environment"
        if 'searchsploit ' in command:
            return "searchsploit is not supported in this environment"
        if 'man ' in command:
            return "man is not supported in this environment"

        # Handle xray command formatting
        if "xray" in command and '--poc' in command:
            parts = command.split()
            new_parts = []
            skip_next = False
            for part in parts:
                if skip_next:
                    skip_next = False
                    continue
                if part == '--poc':
                    skip_next = True
                else:
                    new_parts.append(part)
            command = ' '.join(new_parts)

        try:
            # Execute command with timeout
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            try:
                stdout, stderr = process.communicate(timeout=self.timeout)
                return stdout + stderr
            except subprocess.TimeoutExpired:
                process.kill()
                return "Command execution timeout!"

        except Exception as e:
            return f"Error executing command: {str(e)}"

    def close(self):
        # No resources need explicit closing here, but method retained for symmetry
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

if __name__ == '__main__':
    # Example usage of the InteractiveShell class
    with InteractiveShell(timeout=10) as shell:
        print("=" * 60)
        print(shell.execute_command("pwd"))
        print(shell.execute_command("ls -l"))
        print(shell.execute_command("echo 'Hello, World!'"))
        # You can add more commands here

