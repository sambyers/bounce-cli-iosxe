import sys
import time
from cli import configurep

# First argument in python3 command
interface = sys.argv[1]
# Second agrument in python3 command, cast to int
seconds = int(sys.argv[2])

# Warning
warning = input(f'Interface {interface} is about to be bounced with a {seconds} second delay. Are you sure? (y/n)')
warning = warning.strip()
warning = warning.lower()
if not warning == 'y':
    exit()

# Send config snippet to shutdown the interface
configurep([f'interface {interface}', "shutdown", "end"])
# Sleep for defined number of seconds
time.sleep(seconds)
# Send config snippet to no shutdown the interface
configurep([f'interface {interface}', "no shutdown", "end"])