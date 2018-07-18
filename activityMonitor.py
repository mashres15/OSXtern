# Code by Maniz Shrestha

import csv, os

""" *******************************************************************
# Setting up CSV Logger
*******************************************************************"""
logFile = open("logs.csv", 'w')
fileWriter = csv.writer(logFile)
fileWriter.writerow(['Step', 'Process ID', 'What Happened?'])
	
""" *******************************************************************
# Data Structure for pid_tab to keep track of pid status
# pid.status 0 means pid not in use
# pid.status 1 means pid in use
*******************************************************************"""

class pidTab():
	def __init__(self, pid, status):
		self.pid = pid
		self.status = status
		
maxPid = 2**16
activePid = []		# Using an activePID list to keep track of active PID to avoid scanning pidList for activePid

""" *******************************************************************
# Method to initialize processMap
*******************************************************************"""

def allocateMap():
	global pidList		# pidList is the map that store the pidTab of a pid which contains the status of the pid
	pidList = [pidTab(i, 0) for i in range(1,maxPid+1)]
	
	# Notify success of allocate map
	if pidList[-1].pid == maxPid:
		return 1
	else:
		return -1
		
""" *******************************************************************		
# Method to allocate/release PID for process ID
*******************************************************************"""

def allocateReleasePid(step, pid):
	#  Allocate pid if not allocated
	if pidList[pid].status == 0:
		pidList[pid].status = 1;
		activePid.append(pid)
		#print("Allocated Process ID: "+ str(pid))
		fileWriter.writerow([step, pid,'Start'])
	
	#  Release pid if allocated
	else:
		pidList[pid].status = 0
		pidList[pid].process = None
		activePid.remove(pid)
		#print("Released Process ID: "+ str(pid))
		fileWriter.writerow([step, pid,'Finish'])

""" *******************************************************************
# Method to return one running PID
*******************************************************************"""

def runningPID():
	if len(activePid) == 0: 
		return 0
	else: 
		return activePid.pop()
		
""" *******************************************************************	
# Main Program
*******************************************************************"""

def main():

	print("\n------Process Activity Monitor------")
	print("-----------OSXtern-----------\n")
	
	print("Please enter the process ID that is started or finished")
	print("Press Enter/Return to finish the input\n")
	
	# Allocate map	
	allocateMap()
	step = 0
	
	# Take process input
	while(True):
		pid = input("PID-> ")
		if pid == "": break
		
		if eval(pid) > 2**16 or eval(pid) < 1:
			print("Invalid PID")
			continue
		
		# Allocate or ReleasePid
		allocateReleasePid(step, eval(pid))
		step += 1
	
	# Printing Output of one remaining PID
	print(runningPID())
	
main()
logFile.close()