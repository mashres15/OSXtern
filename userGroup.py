# Code by Maniz Shrestha

import re

"""--------------------------------------------------------------------------	
############### Defining user as an object ###############
--------------------------------------------------------------------------"""	
class user():
	def __init__(self, name):
		self.name = name

"""------------------------------------------------------------
############### Defining userManager as an object ##############
------------------------------------------------------------"""
class userManager():
	def __init__(self):
		self.groups = {}		# Group containing list of users
		self.userList = []		# List containing all the users
	
	"""------------------------------------------------------------
	########### Method to is a user by a name exists ##############
	------------------------------------------------------------"""
	def isExistingUser(self, name):
		
		for existingUser in self.userList:
			if existingUser.name == name:
				return existingUser
		
		return None
	"""------------------------------------------------------------	
	########### Method to add user ##############
	------------------------------------------------------------"""
	def addUser(self, name, group):
		
		# Check if the user exist
		currentUser = self.isExistingUser(name)	
		
		# Create user if not in the userList
		if not currentUser:
			# Creating a new user and adding to the userList
			self.newUser = user(name)
			self.userList.append(self.newUser)
			currentUser = self.newUser
						
		# checking if the group exists
		if group in self.groups:
				# Check if the user is already in the group
				for groupUser in self.groups[group]:
					if groupUser == currentUser: 
						raise Exception("The user is already in the group.")
				
				# Add the user to the group
				self.groups[group].append(currentUser)
		
		else:
			self.groups[group] = [currentUser]
		
		print("Username "+ name+" added to "+ group+".")
	
	"""--------------------------------------------------------------------------	
	########### Method to is return the list of users in groups	##############
	--------------------------------------------------------------------------"""
	def returnUserGroup(self):
		output = ""
		# Scan all groups and make a list of user for each group
		for group in self.groups.keys():
			output += group
			for user in self.groups[group]:
				output += ", " + user.name
			output +="\n"

		return output
	
	"""--------------------------------------------------------------------------	
	########### Method to rename user ##############
	--------------------------------------------------------------------------"""
	def renameUser(self, oldName, newName):
		updated = False
		for user in self.userList:
			if user.name == oldName:
				user.name = newName
				print("User Name updated")
				updated = True
		if not updated:
			print("-->Error: The username you requested to change does not exist")

	"""--------------------------------------------------------------------------	
	########### Method to remove user from a group ##############
	--------------------------------------------------------------------------"""
	def removeUserGrp(self, name, group):
		try:
			for user in self.groups[group]:
				if user.name == name:
					break
			self.groups[group].remove(user)
			print("The username "+ name + " has been removed from "+ group)
		
		except KeyError:
			print("-->Error: The username or the group does not the exist")

"""--------------------------------------------------------------------------	
	########### Method to validate request from command line ##############
	--------------------------------------------------------------------------"""
def validateAndSplit(request):
	request = request.split(' ')
	
	# Checking to see if the request is of valid
	if len(request) == 1:
		if request[0] not in ['ls', 'Exit', 'exit', 'help']:
			print("Invalid Command Line Request. Type Help to display valid request")
			return
	
	elif len(request) == 3:
		if request[0] not in ['rename','rmguser']:
			print("Invalid Command Line Request. Type Help to display valid request")
			return
	
	for word in request:
		match = re.match('[A-Za-z ]+', word)
		if not match:
			print("Words in the line do not match the pattern [A-Za-z ]+")
			return
	
	return request

"""--------------------------------------------------------------------------	
	########### Method to return help commands ##############
	--------------------------------------------------------------------------"""	
def help():
	print("--------------------------------------------------------------------------")
	print("For adding users type -> username group")
	print("For changing username -> rename old_username new_username")
	print("For removing user from a group -> rmguser username group")
	print("To see the changes type -> ls")
	print("To exit type -> exit")
	print("For help type -> help")
	print("--------------------------------------------------------------------------")
"""--------------------------------------------------------------------------	
	########### The main program ##############
	--------------------------------------------------------------------------"""	
def main():
	user = userManager()
	print("\n------User Group Management Mode------")
	print("-----------Admin Privilege-----------\n")
	
	# Instructions for using the management mode
	help()
	
	running = True
	while(running):
		request = input("Enter your command -> ")
		valRequest = validateAndSplit(request)
		
		if valRequest == None: continue
		
		# Print user groups
		elif valRequest[0] =='ls':
			print("\n-----USER GROUPS---------")
			print(user.returnUserGroup())
		
		# Help information prompt
		elif valRequest[0] =='help':
			help()
		
		# Exit User Manager	
		elif valRequest[0] =='Exit' or valRequest[0] =='exit':
			running = False
			
		# Rename User 	
		elif valRequest[0] == 'rename':
			user.renameUser(valRequest[1], valRequest[2])
		
		# Remove User from a group
		elif valRequest[0] == 'rmguser':
			user.removeUserGrp(valRequest[1], valRequest[2])
		
		# Else add new user		
		else:
			user.addUser(valRequest[0], valRequest[1])
			
main()
	