import sys
import encryption_functions
from main import CLA, CTF

# print("Hello world, I'm python code running on the CLA")

CLA = CLA(loadIDs=True)
CTF = CTF(loadIDs=True)

encryption_functions.aes_key_exchange_with_rsa(CLA, CTF)
encrypted_ID_list = CLA.encryptIDList()
CTF.decryptIDList(encrypted_ID_list, CLA.publicKeyRSA())

CLA.saveIDListToFile()
CTF.saveIDListToFile()