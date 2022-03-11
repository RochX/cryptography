import sys

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from main import CLA,CTF

#print("[python] CLA received: " + str(sys.argv[1]) + " " + str(sys.argv[2]) + " " + str(sys.argv[3]))

CTF = CTF()

# Method to convert user submitted data as string

# Method to encrpyt user passed data

# Method to decrypt user passed data in CLA

# Method to convert decrypted data to proper format

CLA.validate()

# Encrypt ID

# Decrypt ID to print
