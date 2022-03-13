import sys
import pickle
import filenames
import encryption_functions
from main import CLA, CTF, Voter

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
pickle.dump(CLA, CLAPickle)
CLAPickle.close()

CTFPickle = open(filenames.CTF, 'wb')

# source, destination
pickle.dump(CTF, CTFPickle)
CTFPickle.close()