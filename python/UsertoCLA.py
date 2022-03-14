import sys
import encryption_functions
from main import CLA, Voter

#print("[python] CLA received: " + str(sys.argv[1]) + " " + str(sys.argv[2]) + " " + str(sys.argv[3]))

Voter = Voter(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))

CLA = CLA(loadIDs=True)

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
    validationMessage = "Invalid Personal Info."

CLA.saveIDListToFile()

print(validationMessage)
