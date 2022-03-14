# Cryptography Final Project: Virtual Election Booth
**Authors:** *Ronan Wolfe, Aleksandr Molchaign, Xavier Silva*

This project is an implementation of a secure electronic voting method.

DISCLAIMER: This system is not viable for actual use! 
It all runs locally on your own machine and is for educational purposes only!

## Voting Process
We have two organizations:
- CLA: Central Legitimization Agency
- CTF: Central Tabulating Facility

A voter will communicate with both organizations in order to vote.

Let Alice be some voter who wants to vote for the candidate Charlie.
The following outlines the process for voting.

### Getting an ID number from the CLA
When a voter wants to vote, they first must get an ID number from the CLA.

Alice and CLA will first establish a secure connection using the RSA Key Exchange and *AES*.
Alice will then request an ID number from the CLA, securing sending this request along with her full name and social security number.

The CLA has a database of people in the population and their social security numbers.
They then use this database to verify that the ID request is really coming from Alice and not someone impersonating her.
This database also has the purpose of verifying Alice is someone who can vote.

The CLA will randomly generate an ID such that no one can randomly guess it.
- This ID will be a random number in the range of 0 to 2^64-1.

They will send this ID back to Alice while also creating a dictionary that relates IDs to voter information.

Now Alice has her ID number.

### CLA giving IDs to CTF
After the CLA has registered all potential voters, they will send a list of all ID numbers (without voter information!) to the CTF.
The CTF marks all of these ID numbers as having not voted yet.

### Casting a Vote, Communicating with the CTF
If Alice wants to vote, she will communicate with the CTF.
Alice and the CTF will first establish a secure connection using the RSA Key Exchange and *AES*.

Say Alice wants to vote for Charlie.
In order to cast her vote, Alice will first create a random nickname for herself; she will use this to identify her vote later.
Alice now sends her vote, ID number, and nickname to the CTF.
The CTF will mark the received ID as having voted and puts the nickname into a list of all nicknames who have voted for Charlie.

Since only Alice knows her nickname and communication is done securely with *AES*, no one can impersonate her or change her vote.

### Post-Voting
After all votes have been cast, the CTF will announce the winner and will also publish the list of nicknames who voted for each candidate.

Alice can look through the list of nicknames of people who voted for Charlie and verify that her vote was counted properly.
However, no one else will know what Alice voted for, since only Alice knows her nickname.
