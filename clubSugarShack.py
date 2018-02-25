#!/usr/bin/env python

import sqlite3
import os
from passlib.hash import sha256_crypt
import getpass


# WORKS WITH PYTHON 3
# THIS SCRIPT LETS YOU SIGN UP, SIGN IN, VIEW MEMBERS
# FIND MEMBERS AND DELETE MEMBERS FROM A MENU.
# IT USES A SQLITE3 DATABASE WITH HASHED PASSWORDS
# WELCOME TO CLUB SUGARSHACK!

#FUNKTIONS
def details():

	fname = input("Enter Firstname: ").lower()
	lname = input("Enter Lastname: ").lower()
	fword = getpass.getpass(prompt="Enter Password: ")
	pword = getpass.getpass(prompt="Re-Enter Password: ")
	return(fname,lname,fword,pword)

def sign_up():

	fname,lname,fword,pword = details()

	try:
		with sqlite3.connect('SugarShack.db') as conn:
			c = conn.cursor()
			os.system('clear')

			c.execute("""CREATE TABLE IF NOT EXISTS user (
			ID INTEGER PRIMARY KEY,
			firstname TEXT NOT NULL,
			lastname TEXT NOT NULL,
			password TEXT NOT NULL)
			""")

			print("ADDING NEW MEMBER")

			#ENCRYPT PASSWORD
			if pword == fword:
				shapword = sha256_crypt.encrypt(str(pword))

			# PASS IN A TUPLE AS ARGS
			c.execute("INSERT INTO user (firstname, lastname, password) VALUES(?, ?, ?)", (fname, lname, shapword))

			conn.commit()
			c.close()
			os.system('clear')

	except:
		print("INCORRECT DETAILS..TRY AGAIN!")
		c.close()

def login():

	fname,lname,fword,pword = details()	
	
	try:
		with sqlite3.connect('SugarShack.db') as conn:
			c = conn.cursor()
			os.system('clear')

			print("PENDING!")

	        #GET USERS HASHED PASSWORD KEY FROM DATABASE
			c.execute("SELECT * FROM user WHERE firstname=? AND lastname=?", (fname, lname))
			data = c.fetchone() [3]

			if sha256_crypt.verify(pword, data):
				print("<><><> LOGGING IN <><><>")	
			else:
				print("INCORRECT DETAILS...TRY AGAIN!")

			c.close()

	except:
		print("INCORRECT DETAILS..TRY AGAIN!")
		c.close()

def view_members():

	try:
		with sqlite3.connect('SugarShack.db') as conn:
			c = conn.cursor()
			os.system('clear')
	
			print("<><><> PLAYERS <> HUSTLERS <> PIMPS <><><>")
			print("")

			for row in c.execute("SELECT * FROM user"):
				print('%4s %10s %13s\t%s' % (row[0], row[1], row[2], row[3]))

			print("-"*110)

			c.close()

	except:
		print("INCORRECT DETAILS..TRY AGAIN!")
		c.close()

def check_user():

	try:
		with sqlite3.connect('SugarShack.db') as conn:
			c = conn.cursor()
			os.system('clear')

			print("<><><> TYPE IN THE PLAYER YOU IS ASKING FOR? <><><>")
			ismember = str(input("Please enter lastname: ")).lower()
			print("<><><> RESULTS <><><>")
			print("")

			for row in c.execute("SELECT * FROM user WHERE lastname=?", (ismember,)):
				print('%4s %10s %13s\t%s' % (row[0], row[1], row[2], row[3]))

			print("-"*110)

			c.close()

	except:
		print("INCORRECT DETAILS..TRY AGAIN!")
		c.close()

def delete_user():

	try:
		with sqlite3.connect('SugarShack.db') as conn:
			c = conn.cursor()
			os.system('clear')

			sucker = str(input("Please enter the users ID number: "))
			print("<><><> GET THE HELL OUTTA MY CLUB! <><><>")

			mydata = c.execute("DELETE FROM user WHERE ID=?", (sucker,))
			conn.commit()
			c.close()		

	except:
		print("INCORRECT DETAILS..TRY AGAIN!")
		c.close()

############### SCRIPT STARTS HERE ####################

def Main():

	while True:
		print ("""
	WELCOME TO CLUB SUGAR SHACK

		1. Become a member
		2. Login
		3. Lookup a player
		4. See all the players		
		5. Remove a player
		6. Exit/Quit
		""")

		ans = input("<><><> PICK A NUMBER <><><> ") 
		if ans == "1": 
			print("\n<><><> NEED SOME DETAILS <><><>") 
			print("<><><> KNOW WHAT IM SAYING! <><><>")
			sign_up()
		elif ans == "2":login()
		elif ans == "3":check_user()
		elif ans == "4":view_members()
		elif ans == "5":delete_user()
		elif ans == "6":
			print("\nLATERZ! LEAVING DA CLUB!")
			break
		elif ans != " ":
			os.system('clear')
			print("\n<><><> STOP TYPING CRAZY SHIT HOLMES <><><>")


if __name__ == '__main__':
	Main()
