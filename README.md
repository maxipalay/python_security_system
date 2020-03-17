# python_security_system

This project was made as a fast and easy approach at creating a surveillance system using just a Raspberry Pi and an Pi Camera.

Common coding guidelines may not have been followed and system security is not a priority (unencrypted password specified in code and put in memory).

Some tutorials followed are linked in the files.

March 2020


# Usage

The provided "security.sh" is run using linux terminal through ssh in the Raspberry Pi. (./security.sh)
This script is in charge of restarting the process if it dies.

If you do not want to use this sript (perhaps for testing) you can simply do "python3 security_system.py".
