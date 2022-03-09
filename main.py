#!/usr/bin/python

import random
import csv
import sys
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
 
class CTF:
    def __init__(self):
        pass
    
# Class meant to represent the CLA and the functions it may need
class CLA:
    def __init__(self):
        self.auth_dict = {}     # Dictionary of Authorized Voter. This uses their SSN as a key, with an array of their first name, last name and validation number 
        self.ids = {}           # Dictionary of validation Ids that have been generated and will be sent to the CTF
        self.loadVoters()       # Intializes data upon start of program.

    # Function to "Register" a user. It checks if they are a valid voter and have not registered yet, then generated a key.
    def validate(self):
        SSN = input("What is your social security number?\n")
        if SSN in self.auth_dict:
            first = input("What is your first name?\n")
            last = input("What is your last name?\n")
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
                    print("Congrats " + self.auth_dict[SSN][0] + " " + self.auth_dict[SSN][1] + " our verification number is " + str(self.auth_dict[SSN][2]))
                else:
                    print("You're already registered.")
            else:
                print("Your SSN and name does not match the database.")
        else:
            print("The social security number you entered, " + SSN + ", is not valid")

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

if __name__ == '__main__':
    
    # First Time Setup at program start
    CLA = CLA()
    print("Welcome to the Virtual Voting Booth!")
    running = True
    
    # Interactable user loop.
    while (running):
        menuChoice = input("Please type the number associated with the action below.\n1. Register to Vote\n2. Vote for a Candidate\n3. Reset Voting Pool\n4. Quit\n")

        if (menuChoice == '1'):
            CLA.validate()
            print("You're Registered!\n")
        elif (menuChoice == '2'):
            print("You've Voted!\n")
        elif (menuChoice == '3'):
            CLA.saveVoters(True)
            print("Voting Data Reset")
        elif (menuChoice == '4'):
            print("Program Terminating\n")
            running = False
        else:
            print(menuChoice + " is not a viable option. Please select an option from the list.")