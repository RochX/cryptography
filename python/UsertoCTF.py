import sys
import pickle
import filenames
import main
import encryption_functions

#print("Hello world, I'm python code running on the CTF")

Voter = Voter("000000000","This is an object for voting","This is an object for voting (lastname)")

CTFfile = open(filenames.CTF, 'rb')     
CTF = pickle.load(CTFfile)
CTFfile.close()

Voter.desired_candidate = sys.argv[1]
Voter.voter_id = sys.argv[2]
Voter.nickname = sys.argv[3]

# Setup key exchange
encryption_functions.aes_key_exchange_with_rsa(CTF,Voter)

# Encrypt using vote data
EncryptedVote = Voter.encrypt_vote()

# argv[1] = candidate choice, argv[2] = user id, argv[3] = username
voteMessage = CTF.vote_from_voter_message(EncryptedVote,Voter.publicKeyRSA())

voteMessage = Voter.decrypt_vote_result(voteMessage,CTF.publicKeyRSA())

CTFPickle = open(filenames.CTF, 'ab')

# source, destination
pickle.dump(db, CTFPickle)                     
CTFPickle.close()

print(voteMessage)