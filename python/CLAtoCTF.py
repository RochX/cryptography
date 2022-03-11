import sys

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from main import CLA,CTF

# print("Hello world, I'm python code running on the CLA")

CLA = CLA()
CTF = CTF()

# Method to convert dictionary of CLA ids to string

# Encrypt converted string

CLA.sendIDs()

# CTF Decryption

# CTF Convert to Dictionary