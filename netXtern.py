import re, csv, time, os
from bs4 import BeautifulSoup
from urllib.request import urlopen

# Code by Maniz Shrestha
# NetXtern

""" *******************************************************************
# Setting up CSV Logger
*******************************************************************"""
logFile = None
if os.path.exists("browseHistory.csv"):
	logFile = open("browseHistory.csv", 'a')
	fileWriter = csv.writer(logFile)
	fileWriter.writerow([])
	
else:
	logFile = open("browseHistory.csv", 'w')
	fileWriter = csv.writer(logFile)
	fileWriter.writerow(['TimeStamp', 'URL'])
	

""" *******************************************************************
# Using Node to store urls
*******************************************************************"""

class Node():
    def __init__(self, url=None, next=None, prev=None):
        self.next = next
        self.prev = prev
        self.url = url

""" *******************************************************************
# Using Node to store keep track of forward and backward links
# BrowseList is a tweak doublylinked list with a lot of additions for browser data structure
*******************************************************************"""

class BrowseList():
	# Constructor
	def __init__(self):
		self.head = self.currentNode = self.tail = Node()
	
	# Method to browse given URL and keep track of the changes in the structure
	def browse(self, url):
		newNode = Node(url)
			
		if self.currentNode.url == None:
			self.tail = self.currentNode = newNode
			self.head.next = newNode
			newNode.prev = self.head
	
		elif self.currentNode != self.tail:
			newNode.prev = self.currentNode
			newNode.next = None
			self.currentNode.next = newNode
			self.tail = newNode
			self.currentNode = newNode
	
		else:
			newNode.prev = self.tail
			newNode.next = None
			self.tail.next = newNode
			self.tail = newNode
			self.currentNode = newNode
	
	# Method to do BACK Operation in the data structure
	def back(self):
		# if current is not the first element
		if self.currentNode != self.head:
			self.currentNode = self.currentNode.prev
	
	# Method to do FORWARD Operation in the data structure	
	def forward(self):
		# if current is not the last element
		if self.currentNode != self.tail:
			self.currentNode = self.currentNode.next
	
	# Print the list of record urls in the BrowseList 		
	def printBrowseList(self):
		pointNode = self.head
		while(True):
			print(" -> " + pointNode.data , end="")
			if pointNode == self.tail: break
			pointNode = pointNode.next
		print()
		
""" *******************************************************************
# Method to print links in a Page
*******************************************************************""" 

def printPageLinks(url):
	fh = urlopen(url)
	html = fh.read()
	fh.close()

	soup = BeautifulSoup(html)
	print()
	for links in soup.find_all('a'):
		print (links.get('href'))
	print()

""" *******************************************************************
# Method to print commands and help for the user interface
*******************************************************************""" 
def help():
	print("--------------------------------------------------------------------------")
	print("-> absolute URL or relative path or absolute path    # Browse the given URL")
	print("  -> https://google.com   # Browse Absolute URL")
	print("  -> /search   # Browse Absolute Path")
	print("  -> privacy   # Browse Relative URL\n")
	
	print("->BACK      	# Browse Back history")
	print("->FORWARD   	# Browse Forward history")
	print("->\ls		# See the links of links in the current page")
	print("To exit type -> \exit")
	print("For help type -> \help")
	
	print("--------------------------------------------------------------------------")


""" *******************************************************************
# The main program
*******************************************************************""" 		
def main():
	print("\n----------------OSXtern----------------")
	print("-----------Process Activity Monitor-----------\n")
	
	help()
	
	print("Please Enter your Absolute URLs, Absolute Paths and Relative Paths in the prompt below:\n")
	
	br = BrowseList()
	
	# --------------------------------------------------------------------------------------------
	# Method that is used to browse a path that is not from homepage
	# --------------------------------------------------------------------------------------------
	def browser(path):
	
		pathMatch = re.match('(\/[A-Za-z0-9]+)+', path)
		relativeMatch = re.match('([A-Za-z0-9]+)(\/[A-Za-z0-9]+)*', path)
		urlMatch = re.match('https:\/\/[A-Za-z0-9]+\.com', path)
	
		currentUrl = br.currentNode.url
		
		# If path is Absolute URL
		if urlMatch:
			currentUrl = path
	
		# BACK operation
		elif path == "BACK":
			br.back()
			# Return current URL
			return br.currentNode.url
	
		# FORWARD operation
		elif path == "FORWARD":
			br.forward()
			# Return current URL
			return br.currentNode.url
	
		# If path is Absolute Path	
		elif pathMatch:
			currentUrl += path
		
		# If path is Relative Path	
		elif relativeMatch:
			# Adding '/' for the query
			path = '/' + path
			currentUrl += path
		
		# print all links in the currentPage
		elif path=="\ls":
			printPageLinks(currentUrl)
			return None
		
		# print help
		elif path=="\help":
			help()
			return None
	
		# If not valid URL
		else:
			print("The path or URL is invalid")
			return None
	
		# Browse and set new URL
		br.browse(currentUrl)
	
		# Return current URL
		return currentUrl
	
	# --------------------------------------------------------------------------------------------
	# Method that is used to browse a path that is from homepage	
	# --------------------------------------------------------------------------------------------
	def homeBrowser(path):
		urlMatch = re.match('https:\/\/[A-Za-z0-9]+\.com', path)
			
		if urlMatch:
			br.browse(path)
			# Return current URL
			return path
			
		# BACK operation
		elif path == "BACK":
			print("Already in Home page.")
			return None

		# FORWARD operation
		elif path == "FORWARD":
			br.forward()
			print("No Forward history")
			# Return current URL
			return br.currentNode.url
		
		# print no links for homepage
		elif path == "\ls":
			print("There are no links in the homepage")
			
		# print help
		elif path=="\help":
			help()
			return None
		
		# If not valid URL
		else:
			print("The path or URL is invalid")
			return None
	
	# --------------------------------------------------------------------------------------------
	# Running Browser			
	# --------------------------------------------------------------------------------------------	
	while(True):
		path = ''
		
		# if browse is in homepage
		if br.currentNode.url == None:
			path = input("Home -> ")
			if path.rstrip() == "\exit": break
			currentURL = homeBrowser(path)
			
		# If it is not in homepage
		else:
			path = input(br.currentNode.url + " -> ")
			# EXIT operation
			if path.rstrip() == "\exit": break
			currentURL = browser(path)
		
		if currentURL:
			now= time.strftime("%c") 
			fileWriter.writerow([now, currentURL])
					
main()
logFile.close()	
	