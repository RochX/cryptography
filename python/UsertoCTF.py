import sys

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from main import CLA,CTF

#print("Hello world, I'm python code running on the CTF")

CTF = CTF()

# Method to convert user data to string

# Encrypt using vote data

# argv[1] = candidate choice, argv[2] = user id, argv[3] = username
CTF.vote(sys.argv[1],sys.argv[2],sys.argv[3])