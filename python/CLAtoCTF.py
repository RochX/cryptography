import sys

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from main import CLA,CTF

# print("Hello world, I'm python code running on the CLA")

CLAfile = open(filenames.CLA, 'rb')     
CLA = pickle.load(CLAfile)
CLAfile.close()
CTFfile = open(filenames.CTF, 'rb')     
CTF = pickle.load(CTFfile)
CTFfile.close()

encryption_functions.aes_key_exchange_with_rsa(CLA, CTF)
encrypted_ID_list = CLA.encryptIDList()
CTF.decryptIDList(encrypted_ID_list, CLA.publicKeyRSA())

CLAPickle = open(filenames.CLA, 'wb')

# source, destination
pickle.dump(db, CLAPickle)                     
CLAPickle.close()

CTFPickle = open(filenames.CTF, 'wb')

# source, destination
pickle.dump(db, CTFPickle)                     
CTFPickle.close()