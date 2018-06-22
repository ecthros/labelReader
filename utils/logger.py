import sys

def good(message):
	''' Prints a message with [+] at the front to signify success '''
	print("[+] " + str(message))

def bad(message):
	''' Prints a message with [-] at the front to signify failure '''
	print("[-] " + str(message))

def fatal(failure):
	print("[/] " + str(failure) + " failed, exiting now")
	sys.exit(1)