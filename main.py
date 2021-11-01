import sqlite3


LoggedIn = 0
conn = sqlite3.connect('test.db')

def main():
	print("hello world")
	cursor = conn.execute("SELECT * from `users`")
	for row in cursor:
	   print(row)

	while True:
		command = input("SecurLogin> ")
		commandarray = command.split(' ')
		print(commandarray)
		print(LoggedIn)

		#everyone can use this command, so no need to check LoggedIn
		

		if(LoggedIn == 0):
			#means nobody is logged in
			if(commandarray[0].lower() == "login"):
				Login()
			elif(commandarray[0].lower() == "help"):
				SendHelp(LoggedIn)
			else:
				print("unrecognized command, type help to get some help")

		elif(LoggedIn == 1):
			#Means user is logged in
			if(commandarray[0].lower() == "logout"):
				Logout()
			elif(commandarray[0].lower() == "help"):
				SendHelp(LoggedIn)
			else:
				print("unrecognized command, type help to get some help")


		elif(LoggedIn == 2):
			#Means admin is logged in 
			if(commandarray[0].lower() == "logout"):
				Logout()
			elif(commandarray[0].lower() == "userlist"):
				userlist()
			elif(commandarray[0].lower() == "help"):
				SendHelp(LoggedIn)
			else:
				print("unrecognized command, type help to get some help")


def SendHelp(LoggedIn):
	if(LoggedIn == 0):
		print("help for login")
	elif(LoggedIn == 1):
		print("help for user")
	elif(LoggedIn == 2):
		print("help for admin")
	return

def Login():
	try:
		print("login")
		username = input("Username: ")
		password = input("password: ")
		rfid = 3930 #needs to be changed later
		getSQLData = conn.execute('''SELECT * FROM `users` WHERE user_name = '%s' ''' % username)
		array = getSQLData.fetchall()
		length = len(array)
		for row in array:
			print(row)

		if length > 1:
			print("error: multiple users with this name")
			return
		elif length == 0: 
			print("no user with this username")
			return
		elif length == 1:
			for result in array:
				databasePassword = result[4]
				databaseSalt = result[3]
				databaserfid = result[5]
				role = result[1]
				locked = result[7]
				if locked == 1:
					print("This account is locked, please ask a system administration")
					return
				else:
					print("hello")
					if databasePassword == password and rfid == databaserfid:
						print("authenticated")

						print("logged in")
						global LoggedIn
						if role == '1':
							LoggedIn = 1
						elif role == '2':
							LoggedIn = 2
						return
					else:
						print("invalid credentials")
						return
		else:
			print("hmmm")
	except Exception as error:
		print(error)

def Logout():
	global LoggedIn
	print("you are logged out")
	LoggedIn = 0
	return


def userlist():
	#get userlist
	print("userlist")
	cursor = conn.execute("SELECT * from `users`")
	for row in cursor:
	   print(row)

if __name__ == "__main__":
	main()


