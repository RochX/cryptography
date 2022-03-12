#!/usr/bin/python

import random
import csv
import sys
import os
import encryption_functions
# CLA
# (Dictionary) Database of authorized voters
# First Name, Last Name, SSN, verification

# CTF
# Verification, Canditate, voted


# User "Signs up" generate random verification if valid. Send back encrypted DHE to AES, include signature

# CLA send encrypted list of verification numbers to CTF

# Using their verification numbers, vote with CTF

# CTF publicly prints results


# Virtual Election Booth Project

class Voter(encryption_functions.CryptographyProperties):
    PERSONAL_INFO_PREFIX = b'PERSONAL_INFO'

    def __init__(self, first_name, last_name, ssn):
        super().__init__()

        # these should be set upon object creation
        self.first_name = first_name
        self.last_name = last_name
        self.ssn = str(ssn)

        # these might not be known at object creation time
        self.voter_id = -1
        self.desired_candidate = "Person"
        self.nickname = "Nickname"

    # encrypt personal info in the string format: "PERSONAL_INFO, SSN, FIRST_NAME, LAST_NAME"
    def encrypt_personal_info(self):
        b_ssn = bytearray(self.ssn, encoding='utf-8')
        b_first_name = bytearray(self.first_name, encoding='utf-8')
        b_last_name = bytearray(self.last_name, encoding='utf-8')

        message = Voter.PERSONAL_INFO_PREFIX + b', ' + b_ssn + b', ' + b_first_name + b', ' + b_last_name

        # TODO remove temporary assignment of AES key and IV!
        #self.aes_key = os.urandom(32)
        #self.iv = os.urandom(16)

        return encryption_functions.encrypt_and_sign(message, self.rsa_private_key, self.aes_key, self.iv)

    def decrypt_voter_id(self, ciphertext, cla_rsa_pub_key):
        plaintext = encryption_functions.decrypt_and_verify(ciphertext, cla_rsa_pub_key, self.aes_key, self.iv)
        plaintext = plaintext.split(b', ')

        # assert we got an ID back
        assert plaintext[0] == CLA.ID_MESSAGE_PREFIX

        self.voter_id = plaintext[1].decode()

    # encrypt vote in the string format: "VOTE, ID, CANDIDATE, NICKNAME"
    def encrypt_vote(self):
        b_voter_id = bytearray(str(self.voter_id), encoding='utf-8')
        b_desired_candidate = bytearray(self.desired_candidate, encoding='utf-8')
        b_nickname = bytearray(self.nickname, encoding='utf-8')

        vote = b'VOTE, ' + b_voter_id + b', ' + b_desired_candidate + b', ' + b_nickname

        return encryption_functions.encrypt_and_sign(vote, self.rsa_private_key, self.aes_key, self.iv)


class CTF(encryption_functions.CryptographyProperties):
    def __init__(self):
        super().__init__()

        self.candidates = {"Captain Blackbeard": {}, "Miss Fortune": {}}
        self.ids = {}                                           # Dictionary of validation Ids that have been generated and sent fron CLA
        self.loadTally()

    # TODO fixme: people can still vote multiple times, I tested it and I was able to vote multiple times! -Xavier
    def vote(self,candidate,id,username):
        if int(id) in CTF.ids:
            for key in self.candidates:
                if str(id) in self.candidates[key].keys():
                    return "You already voted."
            for key in self.candidates:
                if key == candidate:
                    self.candidates[key][id] = username
                    self.saveVoteTally(False)
            return "Congrats! You voted!"
        elif len(CTF.ids) == 0:
            return "Voting period has not begun yet.\n"
        else:
            return "You did not register in time.\n"

    def tally(self):
        print("\nVote Tally\n-----------")
        for key in self.candidates:
            print(key + ": " + str(len(self.candidates[key])))

    def loadTally(self):
        self.candidates = {}
        #read csv, and split on "," the line
        csv_file = csv.reader(open('tally.csv', "r"), delimiter=",")

        #loop through the csv list
        for row in csv_file:
            first = True
            user = False
            key = "name"
            for item in row:
                if first:
                    self.candidates[item] = {}
                    first = False
                    key = item
                else:
                    if not user :
                        idName = item
                        user = True
                    else:
                        self.candidates[key][idName] = item
                        user = False

    # Function to save any CTF updates.
    def saveVoteTally(self,reset):
        #read csv, and split on "," the line
        csv_file = csv.reader(open('tally.csv', "r"), delimiter=",")

        # data rows of csv file 
        rows = []

        if reset:
            rows.append(['Captain Blackbeard'])
            rows.append(['Miss Fortune'])
        else:
            for key in self.candidates:
                candidateData = []
                candidateData.append(key)
                for item in self.candidates[key]:
                    print(item)
                    candidateData.append(item)
                    candidateData.append(self.candidates[key][item])
                rows.append(candidateData)

        # name of csv file 
        filename = "tally.csv"
    
        # writing to csv file 
        with open(filename, 'w', newline='') as csvfile:
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 

            # writing the data rows 
            csvwriter.writerows(rows)

    # decrypts the ID list and verifies the signature of the message from the CLA.
    def decryptIDList(self, ciphertext, CLA_rsa_public_key, iv):
        id_list_bytes = encryption_functions.decrypt_and_verify(ciphertext, CLA_rsa_public_key, self.aes_key, iv)
        id_list = id_list_bytes.decode().split(",")
        for id in id_list[1:]:
            self.ids[int(id)] = True
        pass


# Class meant to represent the CLA and the functions it may need
class CLA(encryption_functions.CryptographyProperties):
    ID_MESSAGE_PREFIX = b'VOTER_ID_IS'
    INVALID_PERSONAL_INFO_PREFIX = b'INVALID_PERSONAL_INFO'

    def __init__(self):
        super().__init__()
        self.auth_dict = {}     # Dictionary of Authorized Voter. This uses their SSN as a key, with an array of their first name, last name and validation number
        self.ids = {}           # Dictionary of validation Ids that have been generated and will be sent to the CTF
        self.loadVoters()       # Intializes data upon start of program.

    # Function to "Register" a user. It checks if they are a valid voter and have not registered yet, then generated a key.
    def validate(self, SSN, first, last, raw_output=False):
        if SSN in self.auth_dict:
            if self.auth_dict[SSN][0] == first and self.auth_dict[SSN][1] == last:
                if self.auth_dict[SSN][2] == -1:
                    random.seed(89)
                    idSearch = True
                    while idSearch is True:
                        id = random.randint(0,3000000)
                        if id not in self.ids:
                            self.auth_dict[SSN][2] = id
                            self.ids[id] = True
                            idSearch = False
                    self.saveVoters(False)
                    if raw_output:
                        return CLA.ID_MESSAGE_PREFIX + b', ' + bytes(str(self.auth_dict[SSN][2]), encoding='utf-8')
                    else:
                        return "Congrats " + self.auth_dict[SSN][0] + " " + self.auth_dict[SSN][1] + " your verification number is " + str(self.auth_dict[SSN][2]) + "!"
                else:
                    if raw_output:
                        return CLA.ID_MESSAGE_PREFIX + b', ' + bytes(str(self.auth_dict[SSN][2]), encoding='utf-8')
                    else:
                        return "You're already registered to vote."
            else:
                return "The SSN and name you entered do not match the database pair."
        else:
            return "The social security number you entered, " + SSN + ", is not authorized to vote."

    # validate a voter based on a voter message from a Voter object
    def validate_voter(self, voter_message, voter_rsa_pub_key):
        # decrypt, verify signature, and split our message
        plaintext = encryption_functions.decrypt_and_verify(voter_message, voter_rsa_pub_key, self.aes_key, self.iv)
        voter_info = plaintext.split(sep=b', ')

        # assume we actually received a voter personal info message
        assert voter_info[0] == Voter.PERSONAL_INFO_PREFIX

        # get personal info
        ssn = voter_info[1].decode()
        first = voter_info[2].decode()
        last = voter_info[3].decode()

        # validate voter
        voter_id = self.validate(ssn, first, last, raw_output=True)

        # make our voter id bytes if it is not for some reason
        if type(voter_id) is not bytes:
            voter_id = bytes(voter_id, encoding='utf-8')

        # check if we got an ID or not
        if not voter_id.startswith(CLA.ID_MESSAGE_PREFIX):
            voter_id = CLA.INVALID_PERSONAL_INFO_PREFIX

        # encrypt and sign voter ID and then return it
        return encryption_functions.encrypt_and_sign(voter_id, self.rsa_private_key, self.aes_key, self.iv)



    # Function to load Voter data from the "voter_auth.csv" file
    def loadVoters(self):
        #read csv, and split on "," the line
        csv_file = csv.reader(open('voter_auth.csv', "r"), delimiter=",")

        #loop through the csv list
        for row in csv_file:
            if row[0] != "SSN":
                self.auth_dict[row[0]] = ['N/A','N/A','N/A',-1]
                self.auth_dict[row[0]][0] = row[1]
                self.auth_dict[row[0]][1] = row[2]
                self.auth_dict[row[0]][2] = int(row[3])
                if int(row[3]) != -1:
                    self.ids[int(row[3])] = True

    # Function to save any CLA updates. One boolean parameter to determine if user data is being reset.
    def saveVoters(self,reset):
        #read csv, and split on "," the line
        csv_file = csv.reader(open('voter_auth.csv', "r"), delimiter=",")

        # field names 
        fields = ['SSN', 'first', 'last', 'id'] 
    
        # data rows of csv file 
        rows = []
        
        if reset == True:
            for item in self.auth_dict:
                rows.append( [item,self.auth_dict[item][0],self.auth_dict[item][1],"-1"] )
                self.auth_dict[item][2] = -1
                self.ids = {}
        else:
            for item in self.auth_dict:
                rows.append( [item,self.auth_dict[item][0],self.auth_dict[item][1],self.auth_dict[item][2]] )

        # name of csv file 
        filename = "voter_auth.csv"
    
        # writing to csv file 
        with open(filename, 'w', newline='') as csvfile:
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
        
            # writing the fields 
            csvwriter.writerow(fields) 
        
            # writing the data rows 
            csvwriter.writerows(rows)

    def sendIDs_unencrypted(self, CTF):
        CTF.ids = self.ids
        return "ID list sent\n"


    # encrypts the ID list to send to the CTF
    def encryptIDList(self, iv):
        id_list = [str(x) for x in list(self.ids.keys())]
        id_list_bytearray = bytearray("ID_List, " + ", ".join(id_list), encoding='ascii')

        return encryption_functions.encrypt_and_sign(bytes(id_list_bytearray), self.rsa_private_key, self.aes_key, iv)


if __name__ == '__main__':
    # First Time Setup at program start
    CLA = CLA()
    CTF = CTF()
    print("Welcome to the Virtual Voting Booth!\n")
    running = True
    
    # Interactable user loop.
    while (running):
        menuChoice = input("Please type the number associated with the action below.\n1. Register to Vote\n2. Vote for a Candidate\n3. Reset Voting Pool\n4. CLA sends the ID list to CTF\n5. CTF Tallies Votes\n6. Quit\n")
        menuChoice = menuChoice.strip()

        if (menuChoice == '1'):
            SSN = input("What is your social security number?\n").strip()
            if len(SSN) == 9:
                first = input("What is your first name?\n").strip()
                last = input("What is your last name?\n").strip()
                print(CLA.validate(SSN,first,last))
            else:
                print(SSN + " is not a valid SSN")
        elif (menuChoice == '2'):
            for key in CTF.candidates.keys():
                print(key)
            voteChoice = input("Please type the name exactly as above that you would like to vote for.\n")
            if voteChoice in CTF.candidates:
                ID = input("Please type your verification ID.\n")
                username = input("Please give an anonymous username to see yourself in the tallyboard.\n")
                print(CTF.vote(voteChoice,int(ID),username))
            else:
                print(voteChoice + " is not on the ballot.\n")
        elif (menuChoice == '3'):
            CLA.saveVoters(True)
            CTF.saveVoteTally(True)
            print("Voting Data Reset\n")
        elif menuChoice == '4':
            encryption_functions.aes_key_exchange_with_rsa(CLA, CTF)

            # set up public iv for use with AES
            iv = os.urandom(16)

            encrypted_ID_list = CLA.encryptIDList(iv)
            CTF.decryptIDList(encrypted_ID_list, CLA.publicKeyRSA(), iv)
        elif (menuChoice == '5'):
            CTF.tally()
        elif (menuChoice == '6'):
            print("Program Terminating\n")
            running = False
        elif (menuChoice == 'Print CTF ids'):
            print(CTF.ids)
            print(" ")
        elif (menuChoice == 'Print CTF candidates'):
            print(CTF.candidates)
            print(" ")
        elif (menuChoice == 'Print CLA ids'):
            print(CLA.ids)
            print(" ")
        elif (menuChoice == 'Print CLA auth_dict'):
            print(CLA.auth_dict)
            print(" ")
        else:
            print(menuChoice + " is not a viable option. Please select an option from the list.\n")