LoggedIn = 0

def main():
	print("hello world")
	while True:
		command = input("SecurLogin> ")
		commandarray = command.split(' ')
		print(commandarray)
		print(LoggedIn)

		#everyone can use this command, so no need to check LoggedIn
		if(commandarray[0].lower() == "help"):
			SendHelp(LoggedIn)

		if(LoggedIn == 0):
			#means nobody is logged in
			if(commandarray[0].lower() == "login"):
				Login()

		elif(LoggedIn == 1):
			#Means user is logged in
			if(commandarray[0].lower() == "logout"):
				Logout()


		elif(LoggedIn == 2):
			#Means admin is logged in 
			if(commandarray[0].lower() == "logout"):
				Logout()
			elif(commandarray[0].lower() == "userlist"):
				userlist()
			


def SendHelp(LoggedIn):
	if(LoggedIn == 0):
		print("help for login")
	elif(LoggedIn == 1):
		print("help for user")
	elif(LoggedIn == 2):
		print("help for admin")
	return

def Login():
	print("login")
	global LoggedIn
	LoggedIn = 1
	return

def Logout():
	global LoggedIn
	LoggedIn = 0
	return


def userlist():
	#get userlist
	print("userlist")

if __name__ == "__main__":
	main()


