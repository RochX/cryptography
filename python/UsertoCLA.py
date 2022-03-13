import sys
import pickle
import python.filenames as filenames
from python.main import CLA, Voter, CTF
import python.encryption_functions as encryption_functions

#print("[python] CLA received: " + str(sys.argv[1]) + " " + str(sys.argv[2]) + " " + str(sys.argv[3]))

Voter = Voter(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
CLAfile = open(filenames.CLA, 'rb')     
CLA = pickle.load(CLAfile)
CLAfile.close()

# Setup key exchange
encryption_functions.aes_key_exchange_with_rsa(CLA,Voter)

# Method to convert user submitted data as string
EncryptedVoterInfo = Voter.encrypt_personal_info()

# Method to encrpyt user passed data
EncryptedVoterID = CLA.validate_voter(EncryptedVoterInfo,Voter.publicKeyRSA())

try:
    # Method to decrypt user passed data in CLA
    Voter.decrypt_voter_id(EncryptedVoterID,CLA.publicKeyRSA())

    # Method to convert decrypted data to proper format
    validationMessage = "Your ID is " + Voter.voter_id
    import CLAtoCTF
except AssertionError:
    validationMessage ="Invalid Personal Info."

CLAPickle = open(filenames.CLA, 'wb')

# source, destination
pickle.dump(db, CLAPickle)                     
CLAPickle.close()

print(validationMessage)
