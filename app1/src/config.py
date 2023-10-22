# config.py
import os

# APP1
PORT_APP1 = 5018
DEBUG_APP1 = True
LOGFILE_APP1 = "logs/app1.log"

# APP2
HOSTNAME_APP2 = os.getenv("HOSTNAME_APP2", "server2")
PORT_APP2 = 5019
PATH_APP2 = "sentiment"
