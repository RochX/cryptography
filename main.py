import random
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
    
class CLA:
    def __init__(self):
        self.auth_dict = {'123456789': ['John', 'Doe', -1],
                     '123456790': ['Jane', 'Doe', -1],
                     '123456791': ['Carl', 'Weezer', -1]
                    }
        self.ids = {}
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
                        id = random.randint(0,3000)
                        if id not in self.ids:
                            self.auth_dict[SSN][2] = id
                            self.ids[id] = True
                            idSearch = False
                    print("Congrats " + self.auth_dict[SSN][0] + " " + self.auth_dict[SSN][1] + " our verification number is " + str(self.auth_dict[SSN][2]))
                else:
                    print("You're already registered.")
            else:
                print("Your SSN and name does not match the database.")
        else:
            print("The social security number you entered, " + SSN + ", is not valid")

if __name__ == '__main__':
    
    CLA = CLA()
    print("Welcome to the Virtual Voting Booth!")
    running = True
    
    while (running):
        menuChoice = input("Please type the number associated with the action below.\n1. Register to Vote\n2. Vote for a Candidate\n3. Quit\n")

        if (menuChoice == '1'):
            CLA.validate()
            print("You're Registered!\n")
        elif (menuChoice == '2'):
            print("You've Voted!\n")
        elif (menuChoice == '3'):
            print("Program Terminating\n")
            running = False
        else:
            print(menuChoice + " is not a viable option. Please select an option from the list.")